def book_serializer(book) -> dict:
    return {
        'id':str(book["_id"]),
        'isbn':book["isbn"],
        'title':book["title"],
        'author':book["author"],
        'description':book["description"],
        'url':book["url"],
    }

def books_serializer(books) -> list:
    return [book_serializer(book) for book in books]