from fastapi import FastAPI
from routes.book_routes import book

app = FastAPI()
app.include_router(book)