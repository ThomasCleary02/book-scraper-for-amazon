import asyncio
import logging
from core.scraper import Scraper
from core.crawler import Crawler
from utils.helpers import setup_logging
from config.mongo import MongoDB

async def get_books(search_query: str) -> list:
    book_links = await Crawler.extract_product_links(search_query)
    books = []
    for link in book_links:
        scraper = Scraper(link)
        book_info = await scraper.get_product_info()
        books.append(book_info)
    return books

async def add_books_to_db(books: list, db: MongoDB):
    added = 0
    updated = 0
    for book in books:
        result = await db.add_book(book)
        if result == 1:
            added += 1
        elif result == 2:
            updated += 1
    return {"added": added, "updated": updated}

async def main():
    setup_logging(logging.INFO)
    search_query = "edward steers jr"
    db = MongoDB()  # Initialize the MongoDB instance
    books = await get_books(search_query)
    result = await add_books_to_db(books, db)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
