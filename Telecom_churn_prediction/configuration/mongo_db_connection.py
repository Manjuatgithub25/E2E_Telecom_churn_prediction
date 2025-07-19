import os, sys, pymongo, certifi
from Telecom_churn_prediction.exception import CustomException
from Telecom_churn_prediction.logger import logger
from Telecom_churn_prediction.constants import database_name, mongoDB_URL

ca = certifi.where()

class MongoDBClient:
    """

    Description :   This method exports the dataframe from mongodb feature store as dataframe 

    """
    client = None

    def __init__(self, database_name=database_name):
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(mongoDB_URL)
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {mongoDB_URL} is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logger.info("MongoDB connection succesfull")
        except Exception as e:
            raise CustomException(e,sys)