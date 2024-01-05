from src.sensor.logger import logging
from src.sensor.exception import CustomException
from src.sensor.utils import get_collection_as_df
import sys

def test_logger_exc():
    try:
        logging.info("Test logger")
        a =1/0
        print(a)
    except Exception as e:
        raise CustomException(e,sys) from None

if __name__ == "__main__":
    get_collection_as_df("aps", "sensor")