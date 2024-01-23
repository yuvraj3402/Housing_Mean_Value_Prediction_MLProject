from housing.exception import HousingException 
from housing.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from housing.entity.config_entity import DataTransformationConfig
import os,sys
from housing.constant import *
from housing.util import read_yaml_file,load_data,save_object
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np





class DataTransformation:

    def __init__(self,data_transformation_config:DataTransformationConfig,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact


        except Exception as e:
            raise HousingException(e,sys) from e
        











    def get_data_transformer_object(self)->ColumnTransformer:
        try:
            schema_file_path=self.data_validation_artifact.schema_file_path

            schema_file=read_yaml_file(file_path=schema_file_path)

            numerical_columns=schema_file[NUMERICAL_COLUMN_KEY]
            
            cat_columns=schema_file[CATEGORICAL_COLUMN_KEY]

            num_pipeline=Pipeline(steps=[
                ('impute',SimpleImputer(strategy="median")),
                ('StandardScalar',StandardScaler())
            ])
            
            

            cat_pipeline=Pipeline(steps=[
                ('imputer',SimpleImputer(strategy="most_frequent")),
                ('OneHotEncoder',OneHotEncoder()),
                ('scaler', StandardScaler(with_mean=False))
            ])
            

            Preprocessing=ColumnTransformer([
                ('num_pipeline',num_pipeline,numerical_columns),
                ('cat_pipeline',cat_pipeline,cat_columns)
            ])

            return Preprocessing
        except Exception as e:
            raise HousingException(e,sys) from e 
        












    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            preprocesing_obj=self.get_data_transformer_object()



            training_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path


            schema_file_path=file_path=self.data_validation_artifact.schema_file_path


            train_df=load_data(file_path=training_file_path,schema_file_path=schema_file_path)
            test_df=load_data(file_path=test_file_path,schema_file_path=schema_file_path)

            schema_file=read_yaml_file(file_path=schema_file_path)



            target_column=schema_file[TARGET_COLUMN_KEY]




            input_train_features=train_df.drop(columns=target_column,axis=1)
            target_train_feature = train_df[target_column]


            input_test_features = test_df.drop(columns=[target_column],axis=1)
            target_test_feature= test_df[target_column]





            input_train_features_arr=preprocesing_obj.fit_transform(input_train_features)
            input_test_features_arr=preprocesing_obj.transform(input_test_features)



            train_arr=np.c_[input_train_features_arr,np.array(target_train_feature)]
            test_arr=np.c_[input_test_features_arr,np.array(target_test_feature)]




            transformed_train_dir=self.data_transformation_config.transformed_train_dir
            os.makedirs(transformed_train_dir,exist_ok=True)



            transformed_test_dir=self.data_transformation_config.transformed_test_dir
            os.makedirs(transformed_test_dir,exist_ok=True)



            train_file_name=os.path.basename(training_file_path).replace(".csv",".npz")
            test_file_name=os.path.basename(test_file_path).replace(".csv",".npz")



            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)



            with open(transformed_train_file_path,"wb") as file_obj:
                np.save(file_obj,train_arr)



            with open(transformed_test_file_path,"wb") as file_obj:
                np.save(file_obj,test_arr)


            preprocessed_object_file_path=self.data_transformation_config.preprocessed_object_file_path


            save_object(file_path=preprocessed_object_file_path,obj=preprocesing_obj)

            data_transformation_artifact=DataTransformationArtifact(transformed_train_file_path=transformed_train_file_path,
                                                                    transformed_test_file_path=transformed_test_file_path,
                                                                    preprocessed_object_file_path=preprocessed_object_file_path)
            
            return data_transformation_artifact


        except Exception as e:
            raise HousingException(e,sys) from e