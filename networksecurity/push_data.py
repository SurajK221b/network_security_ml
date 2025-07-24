import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging import logger

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_convertor(self,file_path):
        try:
            logger.info(f"Attempting to read CSV file: {file_path}")
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            logger.info(f"Successfully converted CSV to JSON. Number of records: {len(records)}")
            return records
        except Exception as e:
            logger.error(f"Error in csv_to_json_convertor: {str(e)}")
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            logger.info(f"Attempting to insert {len(records)} records into MongoDB database: {database}, collection: {collection}")
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            logger.info(f"Successfully inserted {len(self.records)} records into MongoDB")
            return(len(self.records))
        except Exception as e:
            logger.error(f"Error in insert_data_mongodb: {str(e)}")
            raise NetworkSecurityException(e,sys)
        
if __name__=='__main__':
    try:
        logger.info("Starting data extraction and MongoDB insertion process")
        FILE_PATH="Network_Data\phisingData.csv"
        DATABASE="NetworkSecurity"
        Collection="NetworkData"
        
        logger.info(f"File path: {FILE_PATH}")
        logger.info(f"Database: {DATABASE}")
        logger.info(f"Collection: {Collection}")
        
        networkobj=NetworkDataExtract()
        records=networkobj.csv_to_json_convertor(file_path=FILE_PATH)
        print(records)
        no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
        print(no_of_records)
        logger.info("Data extraction and insertion process completed successfully")
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise NetworkSecurityException(e,sys)
        


