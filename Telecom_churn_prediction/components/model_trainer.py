import sys
from typing import Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV, cross_val_score
from traitlets import Float

from Telecom_churn_prediction.entity.estimator import TelcoChurnModel
from Telecom_churn_prediction.exception import CustomException
from Telecom_churn_prediction.logger import logger
from Telecom_churn_prediction.utils.main_utils import load_models_from_yaml, load_numpy_array_data, read_yaml_file, load_object, save_object
from Telecom_churn_prediction.entity.config_entity import ModelTrainerConfig
from Telecom_churn_prediction.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact

            
class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: Configuration for data transformation
        """
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config


    def get_top_models(self, x_train, y_train, models_params) -> dict:
        """
        Description : This function trains multiple classification models and get top 4 models for the evolution stage

        """
        model_accuracies = {}

        for model_name, mp in models_params.items():
            model = mp["model"]            
            logger.info("Models training started")                                  
            model.fit(x_train, y_train)
            
            scores = cross_val_score(model, x_train, y_train, cv=5)                  
            print(f" {model_name} Mean Accuracy = {scores.mean():.4f}")         # Checking mean accuracy 
            model_accuracies[model_name] = float(scores.mean())

        logger.info("Models training Completed")   
        top_models = sorted(model_accuracies.items(), key=lambda x: x[1], reverse=True)[:4]
        top_models = dict(top_models)                                           # Top 4 models
        return top_models
    

    def get_evoluted_model_object_and_report(self, x_train, x_test, y_train, y_test, models_params, evolution_models) -> Tuple[float, object, ClassificationMetricArtifact]:
        """
        Description : This function does hyperparameter tuning and with help of stacking classifier it does prediction
                      and the object and metrics will be returned
        """

        try:
            best_tuned_models = []

            for model_name, mp in models_params.items():
                if model_name in evolution_models.keys():
                    logger.info("Models tuning started")
                    logger.info(f"Tuning {model_name}...")
                    
                    model = mp["model"]
                    params = mp["params"]
                    
                    if params:
                        search = GridSearchCV(estimator=model,
                                            param_grid=params,
                                            cv=5,
                                            scoring="accuracy",
                                            n_jobs=-1,
                                            verbose=0)
                        
                        search.fit(x_train, y_train)
                        best_model = search.best_estimator_
                        logger.info(f"Best {model_name} Params: {search.best_params_}")
                        logger.info(f"Best Cross-Val Score: {search.best_score_}")

                        
                    else:
                        best_model = model.fit(x_train, y_train)
                        logger.info(f"{best_model}: No hyperparameters to tune.")
                
                    best_tuned_models.append((model_name, best_model))

            logger.info("Models tuning complete")

            # Using Stacking Classifier
            meta_learner = LogisticRegression()

            logger.info("stacking Classifier training begins with best tuned models value")
            stacking_clf = StackingClassifier(
                estimators=best_tuned_models,
                final_estimator=meta_learner,
                passthrough=False,
                cv=5
            )

            stacking_clf.fit(x_train, y_train)
            classifier_score = stacking_clf.score(x_test, y_test)
            logger.info(f"Stacking Classifier Test Accuracy: {stacking_clf.score(x_test, y_test)}")

            # Evaluation
            y_pred = stacking_clf.predict(x_test)
            logger.info(f"Confusion Matrix:\n, {confusion_matrix(y_test, y_pred)}")
            
            accuracy = accuracy_score(y_test, y_pred) 
            f1 = f1_score(y_test, y_pred)  
            precision = precision_score(y_test, y_pred)  
            recall = recall_score(y_test, y_pred)
            metric_artifact = ClassificationMetricArtifact(f1_score=f1, precision_score=precision, recall_score=recall)
            
            return classifier_score, stacking_clf, metric_artifact
        
        except Exception as e:
            raise CustomException(e, sys) from e
        

    def initiate_model_trainer(self, ) -> ModelTrainerArtifact:
        logger.info("Entered initiate_model_trainer method of ModelTrainer class")
        """
        Description :   This function initiates a model trainer steps

        """
        try:
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)

            x_train, y_train, x_test, y_test = train_arr[:, :-1], train_arr[:, -1], test_arr[:, :-1], test_arr[:, -1]

            models_and_params = load_models_from_yaml(self.model_trainer_config.model_config_file_path)

            top_models = self.get_top_models(x_train, y_train, models_and_params)
            
            model_score, best_model, metric_artifact = self.get_evoluted_model_object_and_report(x_train, x_test, y_train, y_test, models_and_params, top_models)
            
            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)


            if model_score < self.model_trainer_config.expected_accuracy:
                logger.info("No best model found with score more than base score")
                raise Exception("No best model found with score more than base score")

            churn_model = TelcoChurnModel(preprocessing_object=preprocessing_obj,
                                       trained_model_object=best_model)
            
            logger.info("Created usvisa model object with preprocessor and model")
            logger.info("Created best model file path.")
            save_object(self.model_trainer_config.trained_model_file_path, churn_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact)
            
            logger.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        
        except Exception as e:
            raise CustomException(e, sys) from e