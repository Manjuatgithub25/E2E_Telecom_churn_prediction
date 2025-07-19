import sys

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTENC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer

from Telecom_churn_prediction.constants import  schema_file_path, target_column, column_required_type_change
from Telecom_churn_prediction.entity.config_entity import DataTransformationConfig
from Telecom_churn_prediction.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact, DataValidationArtifact
from Telecom_churn_prediction.exception import CustomException
from Telecom_churn_prediction.logger import logger
from Telecom_churn_prediction.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file, drop_columns



class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=schema_file_path)

        except Exception as e:
            raise CustomException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise CustomException(e, sys)

    
    def get_data_transformer_object(self, ohe_columns, num_features) -> ColumnTransformer:
        """
        Description :   This method creates and returns a data transformer object for the data

        """
        logger.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )

        try:
            logger.info("Got numerical cols from schema config")

            numeric_transformer = StandardScaler()
            oh_transformer = OneHotEncoder()

            logger.info("Initialized StandardScaler, OneHotEncoder, OrdinalEncoder")

            preprocessor = ColumnTransformer(
                [
                    ("StandardScaler", numeric_transformer, num_features),
                    ("OneHotEncoder", oh_transformer, ohe_columns),
                ]
            )

            logger.info("Created preprocessor object from ColumnTransformer")

            logger.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Description :   This method initiates the data transformation component for the pipeline 

        """
        try:
            if self.data_validation_artifact.validation_status:
                logger.info("Starting data transformation")

                train_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.train_data_file_path)
                test_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_data_file_path)

                # Remove blank value rows
                train_df = train_df[~train_df.apply(lambda row: (row == " ").any(), axis=1)]
                test_df = test_df[~test_df.apply(lambda row: (row == " ").any(), axis=1)]

                # Change mismatched column type
                train_df[column_required_type_change] = train_df[column_required_type_change].astype("float64")
                test_df[column_required_type_change] = test_df[column_required_type_change].astype("float64")

                drop_cols = self._schema_config['drop_columns']

                # split train data between input and target features
                input_feature_train_df = train_df.drop(columns=[target_column], axis=1)
                target_feature_train_df = train_df[target_column]
                logger.info("drop the columns in drop_cols of Training dataset")
                input_feature_train_df = drop_columns(df=input_feature_train_df, cols = drop_cols)
                
                # Resample the under sampled class rows for train data
                train_cat_features = input_feature_train_df.select_dtypes(include=["object"]).columns
                categorical_features = [input_feature_train_df.columns.get_loc(col) for col in train_cat_features]
                smote_nc = SMOTENC(categorical_features=categorical_features, random_state=42)

                logger.info("Applying SMOTENC on Training dataset")
                input_feature_train_df_sampled, target_feature_train_df_sampled = smote_nc.fit_resample(input_feature_train_df, target_feature_train_df)
                logger.info("Applied SMOTENC on training dataset")
                logger.info(f"size of train_data: {input_feature_train_df_sampled.shape}")

                # split test data between input and target features
                input_feature_test_df = test_df.drop(columns=[target_column], axis=1)
                target_feature_test_df = test_df[target_column]
                logger.info("drop the columns in drop_cols of Test dataset")
                input_feature_test_df = drop_columns(df=input_feature_test_df, cols = drop_cols)

                # Resample the under sampled class rows for test data
                logger.info("Applying SMOTENC on Testing dataset")
                input_feature_test_df_sampled, target_feature_test_df_sampled = smote_nc.fit_resample(input_feature_test_df, target_feature_test_df)
                logger.info("Applied SMOTENC on testing dataset")
                logger.info(f"size of test_data: {input_feature_test_df_sampled.shape}")
                logger.info("Got train features and test features of Testing dataset")

                num_features = input_feature_train_df_sampled.select_dtypes(exclude=["object"]).columns
                ohe_columns = input_feature_train_df_sampled.select_dtypes(include=["object"]).columns

                label_encoder = LabelEncoder()
                preprocessor = self.get_data_transformer_object(ohe_columns, num_features)
                logger.info("Got the preprocessor object")

                logger.info(
                    "Applying preprocessing object on training dataframe and testing dataframe"
                )

                input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df_sampled)
                target_feature_train_arr = label_encoder.fit_transform(target_feature_train_df_sampled)

                logger.info(
                    "Used the preprocessor object to fit transform the train features"
                )

                input_feature_test_arr = preprocessor.transform(input_feature_test_df_sampled)
                target_feature_test_arr = label_encoder.transform(target_feature_test_df_sampled)

                logger.info("Used the preprocessor object to transform the test features")

                train_arr = np.c_[
                    input_feature_train_arr, np.array(target_feature_train_arr)
                ]

                test_arr = np.c_[
                    input_feature_test_arr, np.array(target_feature_test_arr)
                ]

                logger.info("Created train array and test array")

                save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

                logger.info("Saved the preprocessor object")

                logger.info(
                    "Exited initiate_data_transformation method of Data_Transformation class"
                )

                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )
                return data_transformation_artifact
            else:
                raise Exception(self.data_validation_artifact.message)

        except Exception as e:
            raise CustomException(e, sys) from e