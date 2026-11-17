import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
            db_name = os.getenv("DB_NAME", "escom_db")
            cls._instance.client = MongoClient(mongo_uri)
            cls._instance.db = cls._instance.client[db_name]
        return cls._instance

    def get_collection(self, collection_name: str):
        return self.db[collection_name]