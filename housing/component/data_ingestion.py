from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataIngestionConfig
from housing.entity.artifact_entity import DataIngestionArtifact
from six.moves import urllib
import tarfile
import pandas as pd
import numpy as np
import os,sys
from sklearn.model_selection import StratifiedShuffleSplit


class DataIngestion:


    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise HousingException(e,sys) from e
        

    def download_dataset_url(self):
        try:
            download_url=self.data_ingestion_config.dataset_download_url

            tgz_download_dir=self.data_ingestion_config.tgz_download_dir

            os.makedirs(tgz_download_dir,exist_ok=True)

            file_name="housing.tgz"

            file_path=os.path.join(tgz_download_dir,file_name)
            logging.info(f"downloading file from [{download_url}] in the file [{file_path}]")
            urllib.request.urlretrieve(download_url,file_path)

            return file_path
        except Exception as e:
            raise HousingException(e,sys) from e
        



    def extract_file(self):
        try:
            tgz_download_dir=self.download_dataset_url()
            raw_data_dir=self.data_ingestion_config.raw_data_dir

            with tarfile.open(tgz_download_dir) as housibg_file_obj:
                housibg_file_obj.extractall(path=raw_data_dir)

        except Exception as e:
            raise HousingException(e,sys) from e
        



    def split_data_as_train_test(self)-> DataIngestionArtifact:
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir
            housing_file_name=os.listdir(raw_data_dir)[0]
            housing_file_path=os.path.join(raw_data_dir,housing_file_name)

            housing_data_frame=pd.read_csv(housing_file_path)

            housing_data_frame["income_cat"]=pd.cut(housing_data_frame["median_income"],
                                                    bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                                                    labels=[1,2,3,4,5])
            strat_train_set=None     
            strat_test_set=None        
   
            split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)

            for train_index,test_index in split.split(housing_data_frame,housing_data_frame["income_cat"]):
                strat_train_set=housing_data_frame.loc[train_index].drop(["income_cat"],axis=1)
                strat_test_set=housing_data_frame.loc[test_index].drop(["income_cat"],axis=1)

            train_file_path=os.path.join(self.data_ingestion_config.ingested_train_dir,housing_file_name)
            test_file_path=os.path.join(self.data_ingestion_config.ingested_test_dir,housing_file_name)

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                strat_train_set.to_csv(train_file_path,index=False)

                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                strat_test_set.to_csv(test_file_path,index=False)

                data_ingestion_artifact=DataIngestionArtifact(train_file_path=train_file_path,
                                                              test_file_path=test_file_path)
                
                return data_ingestion_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
        


    def initiate_data_ingestion(self):
        try:
            self.extract_file()

            return self.split_data_as_train_test()
        except Exception as e:
            raise HousingException(os,sys) from e