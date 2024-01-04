import pymongo
import pandas as pd
import json
from pymongo.mongo_client import MongoClient
import ssl


uri = "mongodb+srv://Sethumadhavan:Sethu97@cluster0.mlcteqa.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

DATA_FILE_PATH = "aps_failure_training_set1.csv"
DATABASE_NAME = "aps"
COLLECTION_NAME = "sensor"

if __name__ == "__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Data rows and cols: {df.shape}")

    # convert df to json
    df.reset_index(drop=True, inplace=True)

    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    # Insert data to MogoDb
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)