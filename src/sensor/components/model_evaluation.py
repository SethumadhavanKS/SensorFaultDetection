from src.sensor.utils import utils
from src.sensor.entity import config_entity, artifact_entity
from src.sensor.exception import CustomException
from src.sensor.logger import logging
from src.sensor.model_resolver import ModelResolver
from src.sensor.config import TARGET_COLUMN
from sklearn.metrics import f1_score
import pandas as pd

class ModelEvaluation:

    def __init__(self,model_eval_config:config_entity.ModelEvaluationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                 model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
        logging.info(f"{'>>'*20} Model Evaluation {'<<'*20}")
        self.model_eval_config = model_eval_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_artifact = model_trainer_artifact
        self.model_resolver = ModelResolver()

    def initiate_model_evaluation(self):
        # Compare new model with latest model in saved_models folder
        try:
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            # if no model exist, accept new model
            logging.info("Finding location of existing model")
            if latest_dir_path == None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                                                                              improved_accuracy=None)
                logging("No existing models found, new model accepted")
                return model_eval_artifact
            
            # Finding locations of latest existng model, transformer and encoder
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            # Loading objects
            logging.info("Loading previous model")
            transformer = utils.load_object(transformer_path)
            model = utils.load_object(model_path)
            encoder = utils.load_object(target_encoder_path)


            # Currently trained model objects
            logging.info("Loading current model")
            curr_transformer = utils.load_object(self.data_transformation_artifact.transform_object_path)
            curr_model = utils.load_object(self.model_trainer_artifact.model_path)
            curr_encoder = utils.load_object(self.data_transformation_artifact.target_encoder_path)

            # Loading test data and comparing models
            logging.info("Loading test data")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            input_df = test_df.drop([TARGET_COLUMN])

            # Accuracy of previous model
            input_arr = transformer.transform(input_df)
            y_pred = model.predict(input_arr)
            y_true = encoder.transform(target_df)

            prev_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy of previous model: {prev_model_score}")

            # Accuracy of current model
            input_arr = curr_transformer.transform(input_df)
            y_pred = curr_model.predict(input_arr)
            y_true = curr_encoder.transform(target_df)

            curr_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy of current model: {curr_model_score}")

            if curr_model_score <= prev_model_score:
                logging.info("Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous model")
            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                                                                          improved_accuracy=curr_model_score - prev_model_score)
            logging.info(f"Model evaluation artifact: {model_eval_artifact}")            
            logging.info("Model evaluation completed")

        except Exception as e:
            raise CustomException(e,sys)
        