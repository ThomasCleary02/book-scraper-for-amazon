from config.db import book_info
from schemas.book_schema import books_serializer


def create_book(book):
    _id = book_info.insert_one(dict(book))
    book = books_serializer(book_info.find({ "_id": _id.inserted_id }))
    return { "status": "Ok", "data": book }

book = {
    "isbn"          :   "0813141117",
    "title"         :   "The Trial: The Assassination of President Lincoln and the Trial of the Conspirators",
    "author"        : [ "Edward Steers, Jr." ],
    "description"   :   "On the night of April 14, 1865, John Wilkes Booth assassinated President Abraham Lincoln in what he envisioned part of a scheme to plunge the federal government into chaos and gain a reprieve for the struggling Confederacy. The plan failed. By April 26, Booth was killed resisting capture and eight of the nine conspirators eventually charged in Lincoln's murder were in custody. Their trial would become one of the most famous and most controversial in U.S. history.",
    "url"           :   "https://www.amazon.com/Trial-Assassination-President-Lincoln-Conspirators/dp/0813141117/ref=sr_1_3?crid=FWOO7KBAYSES&dib=eyJ2IjoiMSJ9.YhueyBASCkVVJfjU6ooc8IN5MpZG_BnZQgM54kyjAZzkAcvUSfpQxWkZ6mX-Nq_ol5q5en8Cj9eBQStfELyNqw2O4f5tDPVD_TC7CNETvTPOZaIp10YcyUymq9wfOGGNcMx0eahORWPJ2a26X8fkphUCz3RqthI6Yx5ZteS6Ua0iwZpzexo3Bm46RbfvPEtkmcC5EflFxQLuAa3AijYW9JL6qrOseg9oGvT7g9YnNNs.c8NtDI0UAruB5wEIo8ivcQc_NfbWtF8LrQKX202c0RU&dib_tag=se&keywords=edward+steers+jr&qid=1712450125&sprefix=edward+steers+jr%2Caps%2C101&sr=8-3"
}

create_book(book)