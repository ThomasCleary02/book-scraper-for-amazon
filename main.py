from web_scraper.scraper import Scraper
from web_scraper.crawler import crawl
from config.mongo import book_info

def add_book(book):
    
    try:
        result = book_info.update_one({"isbn": book['isbn']}, { "$set": dict(book) }, upsert=True)
        if result.upserted_id != None:
            action = 1
        elif result.modified_count > 0:
            action = 2

    except AttributeError:
        return None

    return action

def get_books(search_query):
    book_links = crawl(search_query)

    books = []
    
    for link in book_links:
        book = Scraper(link)
        books.append(book.get_product_info())

    return books

def add_books(books):
    added = 0
    updtd = 0

    for book in books:

        result = add_book(book)

        if result == 1:
            added += 1
        elif result == 2:
            updtd += 1

    return { "added": added, "updated": updtd }
            


if __name__=="__main__":

    search_query = "edward steers jr"
            
    books = get_books(search_query)

    result = add_books(books)

    print(result)





