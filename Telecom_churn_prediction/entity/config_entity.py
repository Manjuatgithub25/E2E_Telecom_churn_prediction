import os
from Telecom_churn_prediction.constants import *
from dataclasses import dataclass
from datetime import datetime

time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

@dataclass
class TrainingPipelineConfig:
    pipelineName = pipeline_name
    artifactDir = os.path.join(artifact_dir, time_stamp)

training_pipeline_config = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    data_ingestion_dir = os.path.join(training_pipeline_config.artifactDir, data_ingestion_dir_name)
    feature_store_file_path = os.path.join(data_ingestion_dir, data_ingestion_feature_store_dir, data_file)
    training_data_file_path = os.path.join(data_ingestion_dir, data_ingestion_ingested_dir, train_data_file)
    testing_data_file_path = os.path.join(data_ingestion_dir, data_ingestion_ingested_dir, test_data_file)
    train_test_split_ratio = data_ingestion_train_test_split_ratio
    collectionName = data_ingestion_collection_name

@dataclass
class DataValidationConfig:
    data_validation_dir = os.path.join(training_pipeline_config.artifactDir, data_validation_dir_name)
    drift_report_file_path = os.path.join(data_validation_dir, data_validation_drift_report_dir, 
                                          data_validation_drift_report_file_name)
    

@dataclass
class DataTransformationConfig:
    data_transformation_dir: str = os.path.join(training_pipeline_config.artifactDir, data_transformation_dir_name)
    transformed_train_file_path: str = os.path.join(data_transformation_dir, data_transformation_transformed_data_dir,
                                                    train_data_file.replace("csv", "npy"))
    transformed_test_file_path: str = os.path.join(data_transformation_dir, data_transformation_transformed_data_dir,
                                                   train_data_file.replace("csv", "npy"))
    transformed_object_file_path: str = os.path.join(data_transformation_dir,
                                                     data_transformation_transformed_object_dir,
                                                     preprocessing_object_file_name)
    

@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str = os.path.join(training_pipeline_config.artifactDir, model_trainer_dir_name)
    trained_model_file_path: str = os.path.join(model_trainer_dir, model_trainer_trained_model_dir, model_file_name)
    expected_accuracy: float = model_trainer_expected_score
    model_config_file_path: str = model_trainer_model_config_file_path


@dataclass
class ModelEvaluationConfig:
    changed_threshold_score: float = model_evaluation_changed_threshold_score
    bucket_name: str = model_bucket_name
    s3_model_key_path: str = model_file_name



@dataclass
class ModelPusherConfig:
    bucket_name: str = model_bucket_name
    s3_model_key_path: str = model_file_name


@dataclass
class TelcoChurnaPredictorConfig:
    model_file_path: str = model_file_name
    model_bucket_name: str = model_bucket_name
