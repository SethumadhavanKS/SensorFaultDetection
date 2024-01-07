import os
from src.sensor.exception import CustomException
from src.sensor.entity.config_entity import MODEL_FILE_NAME, TARGET_ENCODER_OBJ_FILE_NAME, TRANSFORMER_OBJ_FILE_NAME

MODEL_REGISTRY = "saved_models"
TRANSFORMER_DIR_NAME = "transformer"
TARGET_ENCODER_DIR_NAME = "target_encoder"
MODEL_DIR_NAME = "model"

class ModelResolver:

    def __init__(self):
        self.model_registry = MODEL_REGISTRY
        self.transformer_dir_name = TRANSFORMER_DIR_NAME
        self.target_encoder_dir_name = TARGET_ENCODER_DIR_NAME
        self.model_dir_name = MODEL_DIR_NAME

    def get_latest_dir_path(self):

        try:
            dir_names = os.listdir(self.model_registry)
            dir_names = list(map(int,dir_names))
            latest_dir_name = max(dir_names)
            return os.path.join(self.model_registry, f"{latest_dir_name}")
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_latest_model_path(self):

        try:
            latest_dir_name = self.get_latest_dir_path()
            if latest_dir_name == None:
                raise Exception("Model is not available")
            return os.path.join(latest_dir_name,self.model_dir_name,MODEL_FILE_NAME)
        
        except Exception as e:
            raise CustomException(e,sys)
                
    def get_latest_transformer_path(self):

        try:
            latest_dir_name = self.get_latest_dir_path()
            if latest_dir_name == None:
                raise Exception("Transformer is not available")
            return os.path.join(latest_dir_name,self.transformer_dir_name,TRANSFORMER_OBJ_FILE_NAME)
        
        except Exception as e:
            raise CustomException(e,sys)
                
    def get_latest_target_encoder_path(self):

        try:
            latest_dir_name = self.get_latest_dir_path()
            if latest_dir_name == None:
                raise Exception("Target encoder is not available")
            return os.path.join(latest_dir_name,self.target_encoder_dir_name,TARGET_ENCODER_OBJ_FILE_NAME)
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_latest_save_dir_path(self):

        try:
            latest_dir_name = self.get_latest_dir_path()
            if latest_dir_name == None:
                return os.path.join(self.model_registry, "0")
            latest_dir_num = os.path.basename(latest_dir_name)
            return os.path.join(self.model_registry, f"{latest_dir_num+1}")
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_latest_save_model_path(self):
        
        try:
            latest_dir_name = self.get_latest_save_dir_path()
            return os.path.join(latest_dir_name, self.model_dir_name, MODEL_FILE_NAME)
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_latest_save_transformer_path(self):
        
        try:
            latest_dir_name = self.get_latest_save_dir_path()
            return os.path.join(latest_dir_name, self.transformer_dir_name, TRANSFORMER_OBJ_FILE_NAME)
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_latest_save_target_encoder_path(self):
        
        try:
            latest_dir_name = self.get_latest_save_dir_path()
            return os.path.join(latest_dir_name, self.target_encoder_dir_name, TARGET_ENCODER_OBJ_FILE_NAME)
        
        except Exception as e:
            raise CustomException(e,sys)