import os
import sys

import numpy as np
import pandas as pd
from Telecom_churn_prediction.entity.config_entity import TelcoChurnaPredictorConfig
from Telecom_churn_prediction.entity.s3_estimator import TelcoChurnEstimator
from Telecom_churn_prediction.exception import CustomException
from Telecom_churn_prediction.logger import logger
from Telecom_churn_prediction.utils.main_utils import read_yaml_file
from pandas import DataFrame


class TelcoChurnData:
    def __init__(self,
                    gender,
                    SeniorCitizen,
                    Partner,
                    Dependents,
                    tenure,
                    PhoneService,
                    MultipleLines,
                    InternetService,
                    OnlineSecurity,
                    OnlineBackup,
                    DeviceProtection,
                    TechSupport,
                    StreamingTV,
                    StreamingMovies,
                    Contract,
                    PaperlessBilling,
                    PaymentMethod,
                    MonthlyCharges,
                    TotalCharges
                ):
        """
        Telco Churn Data constructor
        Input: all features of the trained model for prediction
        """
        try:
            self.gender = gender
            self.SeniorCitizen = SeniorCitizen
            self.Partner = Partner
            self.Dependents = Dependents
            self.tenure = tenure
            self.PhoneService = PhoneService
            self.MultipleLines = MultipleLines
            self.InternetService = InternetService
            self.OnlineSecurity = OnlineSecurity
            self.OnlineBackup = OnlineBackup
            self.DeviceProtection = DeviceProtection
            self.TechSupport = TechSupport
            self.StreamingTV = StreamingTV
            self.StreamingMovies = StreamingMovies
            self.Contract = Contract
            self.PaperlessBilling = PaperlessBilling
            self.PaymentMethod = PaymentMethod
            self.MonthlyCharges = MonthlyCharges
            self.TotalCharges = TotalCharges

        except Exception as e:
            raise CustomException(e, sys) from e

    def get_telco_churn_input_data_frame(self)-> DataFrame:
        """
        This function returns a DataFrame from TelcoChurnData class input
        """
        try:
            
            telcoChurn_input_dict = self.get_telcoChurn_data_as_dict()
            return DataFrame(telcoChurn_input_dict)
        
        except Exception as e:
            raise CustomException(e, sys) from e


    def get_telcoChurn_data_as_dict(self):
        """
        This function returns a dictionary from TelcoChurnData class input 
        """
        logger.info("Entered get_TelcoChurn_data_as_dict method as TelcoChurnData class")

        try:
            input_data = {
                "gender": [self.gender],
                "SeniorCitizen": [self.SeniorCitizen],
                "Partner": [self.Partner],
                "Dependents": [self.Dependents],
                "tenure": [self.tenure],
                "PhoneService": [self.PhoneService],
                "MultipleLines": [self.MultipleLines],
                "InternetService": [self.InternetService],
                "OnlineSecurity": [self.OnlineSecurity],
                "OnlineBackup": [self.OnlineBackup],
                "DeviceProtection": [self.DeviceProtection],
                "TechSupport": [self.TechSupport],
                "StreamingTV": [self.StreamingTV],
                "StreamingMovies": [self.StreamingMovies],
                "Contract": [self.Contract],
                "PaperlessBilling": [self.PaperlessBilling],
                "PaymentMethod": [self.PaymentMethod],
                "MonthlyCharges": [self.MonthlyCharges],
                "TotalCharges": [self.TotalCharges]
            }

            logger.info("Created TelcoChurn data dict")

            logger.info("Exited get_TelcoChurn_data_as_dict method as TelcoChurnData class")

            return input_data

        except Exception as e:
            raise CustomException(e, sys) from e

class TelcoChurnClassifier:
    def __init__(self,prediction_pipeline_config: TelcoChurnaPredictorConfig = TelcoChurnaPredictorConfig(),) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction the value
        """
        try:
            # self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise CustomException(e, sys)


    def predict(self, dataframe) -> str:
        """
        This is the method of USvisaClassifier
        Returns: Prediction in string format
        """
        try:
            logger.info("Entered predict method of USvisaClassifier class")
            model = TelcoChurnEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            result =  model.predict(dataframe)
            
            return result
        
        except Exception as e:
            raise CustomException(e, sys)