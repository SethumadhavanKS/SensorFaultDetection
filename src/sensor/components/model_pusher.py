from src.sensor.utils.utils import load_object, save_object
from src.sensor.entity import config_entity, artifact_entity
from src.sensor.exception import CustomException
from src.sensor.logger import logging
from src.sensor.model_resolver import ModelResolver
import os,sys

class ModelPusher:

    def __init__(self,model_pusher_config:config_entity.ModelPusherConfig,
                    data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                    model_trainer_artifact:artifact_entity.ModelTrainerArtifact,):
        
        try:
            logging.info(f"{'>>'*20} Model Pusher {'<<'*20}")
            self.model_pusher_config = model_pusher_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_pusher(self):

        try:
            # Load current model
            logging.info("Load model, transformer and encoder")
            transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            model = load_object(self.model_trainer_artifact.model_path)
            encoder = load_object(self.data_transformation_artifact.target_encoder_path)

            # Model pusher dir
            logging.info("Saving objects in model pusher directory")
            save_object(file_path=self.model_pusher_config.pusher_transformer_path, obj=transformer)
            save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)
            save_object(file_path=self.model_pusher_config.pusher_encoder_path, obj=encoder)

            # saved_model dir
            transformer_path = self.model_resolver.get_latest_save_transformer_path()
            model_path = self.model_resolver.get_latest_save_model_path()
            encoder_path = self.model_resolver.get_latest_save_target_encoder_path()

            logging.info("Saving objects in saved_model directory")
            save_object(file_path=transformer_path, obj=transformer)
            save_object(file_path=model_path, obj=model)
            save_object(file_path=encoder_path, obj=encoder)
            logging.info(f"Models saved in path: {os.path.basename(model_path)}")

            model_pusher_artifact = artifact_entity.ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.model_pusher_dir,
                                                                   saved_model_dir=self.model_resolver.model_registry)

            logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            logging.info("Model pusher completed")
            return model_pusher_artifact

        except Exception as e:
            raise CustomException(e,sys)