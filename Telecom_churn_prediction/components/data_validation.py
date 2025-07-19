import json
import sys
import pandas as pd
from pandas import DataFrame

from evidently import Report
from evidently.presets import DataDriftPreset

from Telecom_churn_prediction.exception import CustomException
from Telecom_churn_prediction.logger import logger
from Telecom_churn_prediction.utils.main_utils import read_yaml_file, write_yaml_file
from Telecom_churn_prediction.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from Telecom_churn_prediction.entity.config_entity import DataValidationConfig
from Telecom_churn_prediction.constants import schema_file_path


class DataValidation:

    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_validation_config: configuration for data validation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config =read_yaml_file(file_path=schema_file_path)

        except Exception as e:
            raise CustomException(e,sys)

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        """
        Description :   This method validates the number of columns

        """
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logger.info(f"Is required column present: [{status}]")
            return status
        
        except Exception as e:
            raise CustomException(e, sys)

    def is_column_exist(self, df: DataFrame) -> bool:
        """
        Description :   This method validates the existence of a numerical and categorical columns

        """
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if len(missing_numerical_columns) > 0:
                logger.info(f"Missing numerical column: {missing_numerical_columns}")


            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if len(missing_categorical_columns)>0:
                logger.info(f"Missing categorical column: {missing_categorical_columns}")

            return False if len(missing_categorical_columns) > 0 or len(missing_numerical_columns) > 0 else True
        
        except Exception as e:
            raise CustomException(e, sys) from e
        

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise CustomException(e, sys)
        


    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame, ) -> bool:
        """
        Description :   This method validates if drift is detected
    
        """
        try:
            dataDrift_report =Report(metrics=[DataDriftPreset()]) 

            dataDrift_report.run(reference_data=reference_df, current_data=current_df).save_json("tcp.json")
            
            report = dataDrift_report.run(reference_data=reference_df, current_data=current_df).json()
            json_report = json.loads(report)

            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report)

            n_features = json_report["metrics"][0]["value"]["count"]
            drift_share = json_report["metrics"][0]["value"]["share"]
            n_drifted_features = n_features // drift_share if drift_share > 0 else 0

            logger.info(f"{n_drifted_features}/{n_features} drift detected.")
            drift_status = drift_share > 0
            return drift_status
        
        except Exception as e:
            raise CustomException(e, sys) from e
        

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Description :   This method initiates the data validation component for the pipeline

        """

        try:
            validation_error_msg = ""
            logger.info("Starting data validation")
            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.train_data_file_path),
                                 DataValidation.read_data(file_path=self.data_ingestion_artifact.test_data_file_path))

            status = self.validate_number_of_columns(dataframe=train_df)
            logger.info(f"All required columns present in training dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."

            status = self.validate_number_of_columns(dataframe=test_df)
            logger.info(f"All required columns present in testing dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."

            status = self.is_column_exist(df=train_df)
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."

            status = self.is_column_exist(df=test_df)
            if not status:
                validation_error_msg += f"columns are missing in test dataframe."

            validation_status = len(validation_error_msg) == 0
            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logger.info(f"Drift detected.")
                    validation_error_msg = "Drift detected"
                else:
                    validation_error_msg = "Drift not detected"
            else:
                logger.info(f"Validation_error: {validation_error_msg}")
                

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logger.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys) from e