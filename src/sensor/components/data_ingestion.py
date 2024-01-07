from src.sensor.utils import utils
from src.sensor.entity import config_entity, artifact_entity
from src.sensor.exception import CustomException
from src.sensor.logger import logging
import os, sys, pandas as pd, numpy as np
from sklearn.model_selection import train_test_split

class DataIgestion:

    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_ingestion(self) ->artifact_entity.DataIngestionArtifact:
        try:
            logging.info("Data Ingestion Initiated")
            df:pd.DataFrame = utils.get_collection_as_df(
                self.data_ingestion_config.db_Name,
                self.data_ingestion_config.collection_name
                )
            logging.info(f"Exporting collection data as pandas dataframe")
            df.replace(to_replace="na", value= np.NAN,inplace=True)

            # Store data before split 
            featur_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(featur_store_dir,exist_ok=True)

            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path)
            logging.info(f"Data saved in feature store path {self.data_ingestion_config.feature_store_file_path}")

            # Train test split
            train_df, test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)
            logging.info("Data splitted to train test, file path:")

            # Creating directory to store train test 
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir, exist_ok=True)
            
            # Save train test in csv
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path)

            # Prepare artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )

            logging.info(f"Data ingestion completed")
            return data_ingestion_artifact
        
        except Exception as e:
            raise CustomException(e, sys)