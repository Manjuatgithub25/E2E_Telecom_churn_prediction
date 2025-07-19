import sys
import pandas as pd
import numpy as np
from Telecom_churn_prediction.exception import CustomException
from Telecom_churn_prediction.logger import logger
from Telecom_churn_prediction.configuration.mongo_db_connection import MongoDBClient
from Telecom_churn_prediction.constants import database_name



class DataAccessor:

    def __init__(self) -> None:
        try:
            self.client = MongoDBClient(database_name)
        except Exception as e:
            raise CustomException(e, sys)

    
    def export_collection_as_dataframe(self, collection_name, database_name=None):
        try:
            """
            export entire collectin as dataframe:
            return pd.DataFrame of collection

            """
            if database_name is None:
                collection = self.client.database[collection_name]
            else:
                collection = self.client[database_name][collection_name]

            df = pd.DataFrame(collection.find())
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
         
        except Exception as e:
            raise CustomException(e,sys)