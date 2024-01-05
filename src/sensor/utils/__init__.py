import pandas as pd
import sys
from src.sensor.config import mongo_client
from src.sensor.logger import logging
from src.sensor.exception import CustomException

def get_collection_as_df(db_name:str, collection_name:str):
    try:
        logging.info(f"Reading data from db {db_name} and collection {collection_name}")
        mydb = mongo_client[db_name]
        mycol = mydb[collection_name]
        df = pd.DataFrame(mycol.find())
        logging.info(f"Found columns: {df.columns}")

        if "_id" in df.columns:
            logging.info("Dropping collumn _id")
            df = df.drop("_id", axis = 1)
            logging.info(f"Rows and cols in df :{df.shape}")
        
        return df
    except Exception as e:
        raise CustomException(e, sys)
    