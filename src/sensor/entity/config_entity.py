import os, sys
from src.sensor.exception  import CustomException
from datetime import datetime

FILE_NAME = "sensor.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TEST_SIZE = 0.3

class TrainingPipelineConfig:
    def __init__(self):
        self.artifact_dir = os.path.join(os.getcwd(),"artifact", f"{datetime.now().strftime('%m%d%Y_%H%M%s')}")
class DataIngestionConfig:
    def __init__(self,trainingPipelineConfig:TrainingPipelineConfig):
        self.db_Name = "aps"
        self.collection_name = "sensor"
        self.data_ingestion_dir = os.path.join(trainingPipelineConfig.artifact_dir,"data_ingestion")
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
        self.train_file_path = os.path.join(self.data_ingestion_dir,"feature_store",TRAIN_FILE_NAME)
        self.test_file_path = os.path.join(self.data_ingestion_dir,"feature_store",TEST_FILE_NAME)
        self.test_size = TEST_SIZE

    def to_dict() -> dict:
        try:
            return self.__dict__
        except Exception as e:
            raise CustomException(e,sys)

class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...


