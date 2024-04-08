from dotenv import load_dotenv
from pymongo import MongoClient
import gridfs
import os

load_dotenv()

# import env virables
mongo_uri = os.getenv("MONGO_URI")
database_name = os.getenv("DB_NAME")
book_collection = os.getenv("COLLECTION_NAME")  
file_collection = os.getenv("FILE_COLLECTION")

# create db connection
client = MongoClient(mongo_uri)
db = client[database_name]

# instance of book info database
book_info = db[book_collection]