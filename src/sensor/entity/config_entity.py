import os, sys
from src.sensor.exception  import CustomException
from datetime import datetime

FILE_NAME = "sensor.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TEST_SIZE = 0.3
TRANSFORMER_OBJ_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJ_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"
EXPECTED_TEST_SCORE = 0.7
OVERFITTING_THRESHOLD = 0.1
CHANGE_THRESHOLD = 0.01

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

class DataValidationConfig:

    def __init__(self,traing_pipeline_config:TrainingPipelineConfig):
        self.data_validation_directory = os.path.join(traing_pipeline_config.artifact_dir, "data_validation")
        self.report_file_path = os.path.join(self.data_validation_directory, "report.yml")
        self.missing_threshold = 0.2
        self.base_file_path = os.path.join("aps_failure_training_set1.csv")

class DataTransformationConfig:
     def __init__(self,traing_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_directory = os.path.join(traing_pipeline_config.artifact_dir, "data_transformation")
        self.transform_object_path = os.path.join(self.data_transformation_directory,"transformer",TRANSFORMER_OBJ_FILE_NAME)
        self.transform_train_path = os.path.join(self.data_transformation_directory,"transformed",TRAIN_FILE_NAME)
        self.transform_test_path = os.path.join(self.data_transformation_directory,"transformed",TEST_FILE_NAME)
        self.target_encoder_path = os.path.join(self.data_transformation_directory,"target_encoder",TARGET_ENCODER_OBJ_FILE_NAME)
        
class ModelTrainerConfig:
    def __init__(self,traing_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_directory = os.path.join(traing_pipeline_config.artifact_dir, "model_trainer")
        self.model_path = os.path.join(self.model_trainer_directory,"model",MODEL_FILE_NAME)
        self.expected_test_score = EXPECTED_TEST_SCORE
        self.overfitting_threshold = OVERFITTING_THRESHOLD

class ModelEvaluationConfig:
    def __init__(self,traing_pipeline_config:TrainingPipelineConfig):
        self.change_threshold = CHANGE_THRESHOLD

class ModelPusherConfig:
    def __init__(self,traing_pipeline_config:TrainingPipelineConfig):
        self.model_pusher_dir = os.path.join(traing_pipeline_config.artifact_dir,"model_pusher")
        self.pusher_model_path = os.path.join(self.model_pusher_dir,"transformer",MODEL_FILE_NAME)
        self.pusher_transformer_path = os.path.join(self.model_pusher_dir,"model",TRANSFORMER_OBJ_FILE_NAME)
        self.pusher_encoder_path = os.path.join(self.model_pusher_dir,"target_encoder",TARGET_ENCODER_OBJ_FILE_NAME)