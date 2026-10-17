import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client =MongoClient(os.environ["MONGO_URI"], serverSelectionTimeoutMS=3000)
print("Database:", client.list_database_names())