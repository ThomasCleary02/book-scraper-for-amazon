from fastapi import APIRouter
from models.book_model import Book
from schemas.book_schema import books_serializer
from bson import ObjectId
from config.db import book_info

book = APIRouter()

@book.post("/")
async def create_book(book: Book):
    _id = book_info.insert_one(dict(book))
    book = books_serializer(book_info.find({ "_id": _id.inserted_id }))
    return { "status": "Ok", "data": book }

@book.get("/")
async def get_all_books():
    books = books_serializer(book_info.find())
    return { "status": "Ok", "info": books }

@book.get("/{id}")
async def get_one_book(id: str):
    book = books_serializer(book_info.find( { "_id": ObjectId(id) } ))
    return {"status": "Ok", "data": book}

@book.put("/")
async def update_book(id: str, book: Book):
    book_info.find_one_and_update(
        {
            "_id": ObjectId(id)
        },
        {
            "$set": dict(book)
        })
    book = books_serializer(book_info.find({"_id":ObjectId(id)}))
    return {"status": "Ok", "data": book}

@book.delete("/{id}")
async def delete_book(id: str):
    book_info.find_one_and_delete({"_id": ObjectId(id)})
    books = books_serializer(book_info.find())
    return {"status": "Ok", "data": book}
