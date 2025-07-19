import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from Telecom_churn_prediction.entity.config_entity import DataIngestionConfig
from Telecom_churn_prediction.entity.artifact_entity import DataIngestionArtifact
from Telecom_churn_prediction.exception import CustomException
from Telecom_churn_prediction.logger import logger
from Telecom_churn_prediction.churn_data_access.mongoDB_data_access import DataAccessor



class DataIngestion:

    def __init__(self):
        """
        Intialise object for the required configs

        """
        try:
            self.data_ingestion_config = DataIngestionConfig()             
        except Exception as e:
            raise CustomException(e,sys)
        

    
    def export_data_into_feature_store(self):
        """
        Description :  This method exports data from mongodb to csv file

        """
        try:
            logger.info(f"Exporting data from mongodb")
            churn_data = DataAccessor()
            dataframe = churn_data.export_collection_as_dataframe(self.data_ingestion_config.collectionName)
            logger.info(f"Shape of dataframe: {dataframe.shape}")

            feature_store_file_path  = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logger.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe

        except Exception as e:
            raise CustomException(e,sys)
        

    def split_data_as_train_test(self,dataframe):
        """
        Description :  This method splits the dataframe into train set and test set based on split ratio 
    
        """
        logger.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logger.info("Performed train test split on the dataframe")
            logger.info("Exited split_data_as_train_test method of Data_Ingestion class")
            dir_path = os.path.dirname(self.data_ingestion_config.training_data_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            logger.info(f"Exporting train and test file path.")
            train_set.to_csv(self.data_ingestion_config.training_data_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_data_file_path,index=False,header=True)

            logger.info(f"Exported train and test file path.")
        except Exception as e:
            raise CustomException(e, sys) from e

    
    def initiate_data_ingestion(self):
        """
        Description :  This method initiates the data ingestion components of training pipeline

        """
        logger.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:
            dataframe = self.export_data_into_feature_store()

            logger.info("Got the data from mongodb")

            self.split_data_as_train_test(dataframe)

            logger.info("Performed train test split on the dataset")

            logger.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )

            data_ingestion_artifact = DataIngestionArtifact(self.data_ingestion_config.training_data_file_path,
                                                            self.data_ingestion_config.testing_data_file_path)
            
            logger.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys) from e