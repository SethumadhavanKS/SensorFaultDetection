from src.sensor.logger import logging
from src.sensor.exception import CustomException
from src.sensor.entity import config_entity
from src.sensor.components import data_ingestion, data_validation, data_transformation, model_trainer
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
    # Data ingestion
    data_ingestion_config = config_entity.DataIngestionConfig(trainingPipelineConfig=train_pipeline_config)
    data_ingestion = data_ingestion.DataIgestion(data_ingestion_config=data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

    # Data validation
    data_validation_config = config_entity.DataValidationConfig(traing_pipeline_config=train_pipeline_config)
    data_validation = data_validation.DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
    data_validation_artifact = data_validation.initiate_data_validation()

    # Data Transformation
    data_transformation_config = config_entity.DataTransformationConfig(traing_pipeline_config=train_pipeline_config)
    data_transformation = data_transformation.DataTransformation(data_transformation_config=data_transformation_config,data_ingestion_artifact=data_ingestion_artifact)
    data_transformation_artifact = data_transformation.initiate_data_transformation()

    # Model trainer
    model_trainer_config = config_entity.ModelTrainerConfig(traing_pipeline_config=train_pipeline_config)
    model_trainer = model_trainer.ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
    model_trainer_artifact = model_trainer.initiate_model_trainer()