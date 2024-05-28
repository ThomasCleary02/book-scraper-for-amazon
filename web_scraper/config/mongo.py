from dotenv import load_dotenv
from pymongo import MongoClient
import logging
import os

load_dotenv()

class MongoDB:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI")
        self.database_name = os.getenv("DB_NAME")
        self.book_collection = os.getenv("COLLECTION_NAME")
        
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.database_name]
        self.book_info = self.db[self.book_collection]

    async def add_book(self, book: dict) -> int:
        """
        Add or update book information in the MongoDB collection.

        :param book: Dictionary containing book information.
        :return: 1 if inserted, 2 if updated, None if error occurs.
        """
        try:
            result = self.book_info.update_one({"isbn": book['isbn']}, {"$set": book}, upsert=True)
            if result.upserted_id is not None:
                return 1
            elif result.modified_count > 0:
                return 2
        except Exception as e:
            logging.error(f"Error adding book to database: {e}")
            return None
