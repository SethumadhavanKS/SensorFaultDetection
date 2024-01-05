import pymongo
import pandas as pd
import json
from dataclasses import dataclass

import os

@dataclass
class EnvironmentVariables:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")

env_var = EnvironmentVariables()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
try:
    mongo_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)