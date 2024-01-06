from typing import Optional
from src.sensor.utils import utils
from src.sensor.entity import config_entity, artifact_entity
from src.sensor.exception import CustomException
from src.sensor.logger import logging
from src.sensor.config import TARGET_COLUMN
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from imblearn.combine import SMOTETomek


import os, sys, pandas as pd, numpy as np

class DataTransformation:

    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        
        try:
            simple_imputer = SimpleImputer(strategy='constant', fill_value=0)
            robust_scaler = RobustScaler()
            pipeline = Pipeline(steps=[
                ("Imputer",simple_imputer),
                ("RobustScaler",robust_scaler)
            ])
            return pipeline
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self) -> artifact_entity.DataTransformationArtifact:

        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            input_feature_train_df = train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN,axis=1)

            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            # Transformation on target columns
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)

            # Transforming input features
            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)

            # Baglancing distribution of both category data

            smk = SMOTETomek(sampling_strategy = 'minority')
            logging.info(f"Before sampling Train set Input: {input_feature_train_arr.shape} Target: {target_feature_train_arr.shape}")
            input_feature_train_arr, target_feature_train_arr = smk.fit_resample(input_feature_train_arr, target_feature_train_arr)
            logging.info(f"After sampling Train set Input: {input_feature_train_arr.shape} Target: {target_feature_train_arr.shape}")

            logging.info(f"Before sampling Test set Input: {input_feature_test_arr.shape} Target: {target_feature_test_arr.shape}")
            input_feature_test_arr, target_feature_test_arr = smk.fit_resample(input_feature_test_arr, target_feature_test_arr)
            logging.info(f"After sampling Test set Input: {input_feature_test_arr.shape} Target: {target_feature_test_arr.shape}")

            # Saving transformed train and test data
            train_arr = np.c_(input_feature_train_arr, target_feature_train_arr)
            test_arr = np.c_(input_feature_test_arr,target_feature_test_arr)

            utils.save_numpy_array(self.data_transformation_config.transform_train_path,train_arr)
            utils.save_numpy_array(self.data_transformation_config.transform_test_path,test_arr)

            # Saving transformer and encoder
            utils.save_object(self.data_transformation_config.transform_object_path, transformation_pipeline)
            utils.save_object(self.data_transformation_config.target_encoder_path, label_encoder)

            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transform_train_path=self.data_transformation_config.transform_train_path,
                transform_test_path=self.data_transformation_config.transform_test_path,
                target_encoder_path=self.data_transformation_config.target_encoder_path
            )
            logging.info("Data transformation completed")
            return data_transformation_artifact
        
        except Exception as e:
            raise CustomException(e,sys)