import yaml
from housing.exception import HousingException
from housing.constant import *
import pandas as pd
import os,sys
import dill
import numpy as np





def write_yaml_file(file_path:str,data:dict=None):
   
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise HousingException(e,sys) from e




def read_yaml_file(file_path):
    
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e,sys) from e




def load_data(file_path,schema_file_path):
    try:
        dataframe=pd.read_csv(file_path)


        dataset_schema=read_yaml_file(schema_file_path)

        schema_columns=dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]
        
        for columns in  dataframe.columns:
            if columns in list(schema_columns.keys()):
                dataframe[columns].astype(schema_columns[columns])
            else:
                raise Exception
            return dataframe

    except Exception as e:
        raise HousingException(e,sys) from e





def save_numpy_array_data(file_path: str, array: np.array):

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise HousingException(e, sys) from e





def load_numpy_array_data(file_path: str) :

    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise HousingException(e, sys) from e




def save_object(file_path:str,obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e



def load_object(file_path:str):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e
