from src.sensor.utils import utils
from src.sensor.entity import config_entity, artifact_entity
from src.sensor.exception import CustomException
from src.sensor.logger import logging
from src.sensor.config import TARGET_COLUMN
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import f1_score

class ModelTrainer:

    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                    data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact
    
    def train_model(self,x,y):
        logging.info(f"Traning XGB Classifier")
        xgb_clf = XGBClassifier()
        xgb_clf.fit(x,y)
        return xgb_clf

    def initiate_model_trainer(self):
        try:
            logging.info("Loading train and test array")
            train_arr = utils.load_numpy_array(self.data_transformation_artifact.transform_train_path)
            test_arr = utils.load_numpy_array(self.data_transformation_artifact.transform_test_path)

            logging.info("Splitting input and target feature from train and test array")
            x_train, y_train = train_arr[:,:-1], train_arr[:,-1]
            x_test, y_test= test_arr[:,:-1], test_arr[:,-1]

            model = self.train_model(x=x_train,y=y_train)

            logging.info("Calculating f1 train score")
            yhat_train = model.predict(x_train)
            f1_train_score = f1_score(y_true=y_train, y_pred=yhat_train)

            logging.info("Calculating f1 test score")
            yhat_test = model.predict(x_test)
            f1_test_score = f1_score(y_true=y_test, y_pred=yhat_test)
            logging.info(f"Train f1 score: {f1_train_score}, test f1 score: {f1_test_score}")

            # Check for overfitting or underfitting or expected score
            logging.info("Checking model underfitted or not")
            if f1_test_score < self.model_trainer_config.expected_test_score:
                raise Exception(f"Model is not good as it is not able to give expected score: 
                                {self.model_trainer_config.expected_test_score}, model actual score: {f1_test_score}")

            logging.info("Checking model overfotted or not")
            diff = abs(f1_test_score - f1_train_score)
            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score difference: {diff} is higher than overfitting threshold: {self.model_trainer_config.overfitting_threshold}")
            
            # Saving model
            logging.info("Saving model object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            logging.info("Preparing artifact")
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path,
                                                                          f1_test_score=f1_test_score,
                                                                          f1_train_score=f1_train_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            logging.info("Model Training completed")
            return model_trainer_artifact
        

        except Exception as e:
            raise CustomException(e,sys)