from src.sensor.logger import logging
from src.sensor.exception import CustomException
from src.sensor.entity import config_entity
from src.sensor.components import data_ingestion, data_validation
import sys

def test_logger_exc():
    try:
        logging.info("Test logger")
        a =1/0
        print(a)
    except Exception as e:
        raise CustomException(e,sys) from None

if __name__ == "__main__":

    train_pipeline_config = config_entity.TrainingPipelineConfig()
    data_ingestion_config = config_entity.DataIngestionConfig(trainingPipelineConfig=train_pipeline_config)
    data_ingestion = data_ingestion.DataIgestion(data_ingestion_config=data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

    data_validation_config = config_entity.DataValidationConfig(traing_pipeline_config=train_pipeline_config)
    data_validation = data_validation.DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
    data_validation_artifact = data_validation.initiate_data_validation()