from typing import Optional
from src.sensor.utils import utils
from src.sensor.entity import config_entity, artifact_entity
from src.sensor.exception import CustomException
from src.sensor.logger import logging
from scipy.stats import ks_2samp

import os, sys, pandas as pd, numpy as np

class DataValidation:
    
    def __init__(self, 
                 data_validation_config: config_entity.DataValidationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
        except Exception as e:
            raise CustomException(e,sys)
        
    def drop_missing_values(self,df:pd.DataFrame, report_key_name:str) -> Optional[pd.DataFrame]:

        """ This method will drop columns with null values greater than specified threshold"""

        try:
            missing_threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]

            # Selecting columns which contains null
            logging.info(f"Selecting columns which contains null above to {missing_threshold}")
            drop_column_names = null_report[null_report>missing_threshold].index

            logging.info(f"Columns to drop: {list(drop_column_names)}")
            self.validation_error[report_key_name] = list(drop_column_names)
            df.drop(list(drop_column_names),axis=1, inplace=True)

            # Return None if no columns left
            if len(df.columns) == 0:
                return None
            
            return df
        
        except Exception as e:  
            raise CustomException(e,sys)
        
    def is_required_column_exist(self, base_df:pd.DataFrame, current_df:pd.DataFrame,report_key_name:str):

        try:
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_cols = []
            for base_col in base_columns:
                if base_col not in current_columns:
                    logging.info(f"Column: [{base_col} is not available]")
                    missing_cols.append(base_col)

            if len(missing_cols) > 0:
                self.validation_error[report_key_name] = missing_cols
                return False
            return True
        
        except Exception as e:  
            raise CustomException(e,sys)
        
    def data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, report_key_name:str):

        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns
            for base_col in base_columns:
                base_data, current_data = base_df[base_col], current_df[base_col]
                # Null hypothesis is both data are from same distribution
                same_distribution = ks_2samp(base_data, current_data)

                if same_distribution.pvalue > 0.05:
                    # Accepting null hypothesis
                    drift_report[base_col] = {"pvalue":float(same_distribution.pvalue),
                                              "same_distribution":True}
                else:
                    drift_report[base_col] = {"pvalue":float(same_distribution.pvalue),
                                              "same_distribution":False}
            self.validation_error[report_key_name] = drift_report
        except Exception as e:  
            raise CustomException(e,sys)
        
    def initiate_data_validation(self) -> artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"Reading base df")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            logging.info(f"Replace na in base df")
            base_df.replace({"na":np.NAN},inplace=True)

            logging.info(f"Drop null values columns from base df")
            base_df = self.drop_missing_values(df=base_df, report_key_name="missing_values_in_base_dataset")
            logging.info(f"Reading train and test df")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info(f"Drop null values columns from train and test df")
            train_df = self.drop_missing_values(df=train_df, report_key_name="missing_values_in_train_dataset")
            test_df = self.drop_missing_values(df=test_df,report_key_name="missing_values_in_test_dataset")

            exclude_cols = ["class"]
            base_df = utils.convert_columns_float(df=base_df,exclude_cols=exclude_cols)
            train_df = utils.convert_columns_float(df=train_df,exclude_cols=exclude_cols)
            test_df = utils.convert_columns_float(df=test_df,exclude_cols=exclude_cols)
            
            logging.info(f"Checking all required column present in train and test df")
            train_df_col_status = self.is_required_column_exist(base_df=base_df, current_df=train_df,report_key_name="missing_columns_in_train_dataset")
            test_df_col_status = self.is_required_column_exist(base_df=base_df, current_df=test_df,report_key_name="missing_columns_in_test_dataset")

            if train_df_col_status:
                logging.info(f"As all required columns available in train df, hence detecting dara drift")
                self.data_drift(base_df=base_df,current_df=train_df, report_key_name="data_drift_in_train_dataset")
            if test_df_col_status:
                logging.info(f"As all required columns available in test df, hence detecting dara drift")
                self.data_drift(base_df=base_df,current_df=test_df, report_key_name="data_drift_in_test_dataset")
            
            logging.info(f"Writing reports in YAML file")
            # write report
            utils.write_yaml_file(self.data_validation_config.report_file_path,self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(self.data_validation_config.report_file_path)
            logging.info(f"Data validation completed")
            return data_validation_artifact
        
        except Exception as e:  
            raise CustomException(e,sys)