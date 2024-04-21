from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

# set env variables for mongodb
mongo_uri = os.getenv("MONGO_URI")
database_name = os.getenv("DB_NAME")
book_collection = os.getenv("COLLECTION_NAME")

# create db connection
client = MongoClient(mongo_uri)
db = client[database_name]

# instance of book collection
book_info = db[book_collection]