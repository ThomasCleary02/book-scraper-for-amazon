from schemas.book_schema import books_serializer
from config.db import collection
import json

file = json.load(open('books.json'))

def create_book(book):
    _id = collection.insert_one(dict(book))
    book = books_serializer(collection.find( { "_id" : _id.inserted_id } ))
    return { "status" : "Ok", "data" : book }

for book in file['books']:
    create_book(book)