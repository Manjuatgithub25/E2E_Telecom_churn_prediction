import os
import pandas as pd
from datetime import datetime

database_name = "telecom_churn"

collection_name = "churn_data"

mongoDB_URL = "MongoDB_Cluster0"

pipeline_name = "predict_telecom_churn"
artifact_dir = "artifact"

data_file = "Telco_Customer_Churn.csv"
train_data_file = "train.csv"
test_data_file = "test.csv"

model_file_name = "model.pkl"

target_column = "Churn"
column_required_type_change = "TotalCharges"
preprocessing_object_file_name = "preprocessing.pkl"
schema_file_path = os.path.join("config", "schema.yaml")


aws_access_key_id_env_key = "AWS_ACCESS_KEY_ID"
aws_secret_access_key_env_key = "AWS_SECRET_ACCESS_KEY"
region_name = "ap-south-1"

"""
    Data Ingestion related constants

"""

data_ingestion_collection_name = "churn_data"
data_ingestion_dir_name = "data_ingestion"
data_ingestion_feature_store_dir = "feature_store"
data_ingestion_ingested_dir = "ingested"
data_ingestion_train_test_split_ratio = 0.2


"""
   Data Validation related constants

""" 

data_validation_dir_name = "data_validation"
data_validation_drift_report_dir = "drift_report"
data_validation_drift_report_file_name = "report.yaml"


"""
   Data Transformation related constants

""" 

data_transformation_dir_name = "data_transformation"
data_transformation_transformed_data_dir = "transformed"
data_transformation_transformed_object_dir = "transformed_object"


"""
Model Trainer related constants
"""
model_trainer_dir_name: str = "model_trainer"
model_trainer_trained_model_dir: str = "trained_model"
model_trainer_trained_model_name: str = "model.pkl"
model_trainer_expected_score: float = 0.6
model_trainer_model_config_file_path: str = os.path.join("config", "model.yaml")


"""
MODEL EVALUATION related constant 
"""
model_evaluation_changed_threshold_score: float = 0.02
model_bucket_name = "telcochurn-model2025"
model_pusher_s3_key = "model-registry"


APP_HOST = "0.0.0.0"
APP_PORT = 8080




