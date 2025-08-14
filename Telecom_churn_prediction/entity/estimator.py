from pandas import DataFrame
from sklearn.compose import ColumnTransformer


class TelcoChurnModel:
    def __init__(self, preprocessing_object: ColumnTransformer, trained_model_object: object):
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object
        print("-----------------------------------------------------------------------",self.trained_model_object)

    def predict_output(self, dataframe):
        transformed = self.preprocessing_object.transform(dataframe)
        print("--------------------------------------------------------------------------------",transformed)
        return self.trained_model_object.predict(transformed)
