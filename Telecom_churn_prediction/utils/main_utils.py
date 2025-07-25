import os
import sys
import numpy as np
import dill
import yaml
import importlib
from pandas import DataFrame

from Telecom_churn_prediction.exception import CustomException
from Telecom_churn_prediction.logger import logger


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:    
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise CustomException(e, sys) from e
    


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CustomException(e, sys) from e
    



def load_object(file_path: str) -> object:
    logger.info("Entered the load_object method of utils")

    try:

        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)

        logger.info("Exited the load_object method of utils")

        return obj

    except Exception as e:
        raise CustomException(e, sys) from e
    


def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise CustomException(e, sys) from e
    



def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys) from e




def save_object(file_path: str, obj: object) -> None:
    logger.info("Entered the save_object method of utils")

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logger.info("Exited the save_object method of utils")

    except Exception as e:
        raise CustomException(e, sys) from e



def drop_columns(df: DataFrame, cols: list)-> DataFrame:

    """
    drop the columns form a pandas DataFrame
    df: pandas DataFrame
    cols: list of columns to be dropped
    """
    logger.info("Entered drop_columns methon of utils")

    try:
        df = df.drop(columns=cols, axis=1)

        logger.info("Exited the drop_columns method of utils")
        
        return df
    except Exception as e:
        raise CustomException(e, sys) from e
    


def load_models_from_yaml(yaml_path) -> dict:
    with open(yaml_path, "r") as file:
        config = yaml.safe_load(file)

    models = {}
    for name, info in config.items():
        module = importlib.import_module(info["module"])
        cls = getattr(module, info["class"])
        model_instance = cls(**{k: v for k, v in info.get("params", {}).items() if not isinstance(v, list)})
        models[name] = {
            "model": model_instance,
            "params": info.get("params", {})
        }
    return models

