import uuid
from enum import Enum
from flask import Flask, jsonify, make_response, request
from datetime import date, datetime
import logging

app = Flask(__name__) #“__name__” is a Python special variable which gives Python file a unique name

class BookType(str, Enum):
    SCIENCE_FICTION: str = "Science Fiction"
    SATIRE: str = "Satire"
    DRAMA: str = "Drama"
    ACTION_AND_ADVENTURE: str = "Action and Adventure"
    ROMANCE: str = "Romance"

class Book:
    def __init__(self, book_type, title, creation_date):
        self._book_type = book_type
        self._title = title
        self._id = str(uuid.uuid4())
        if creation_date is not None:
                self._creation_date = creation_date
        else:
            self._creation_date = None

        self._updated_date_time = datetime.now().isoformat()

    def json(self):
        return {"_book_type":self._book_type, "_title":self._title, "_id":self._id, "_creation_date":self._creation_date,
                "_updated_date_time":self._updated_date_time}

def set_books():
    book1 = Book(BookType.ACTION_AND_ADVENTURE, "The Fountainhead", date(1943, 10, 1).isoformat())
    book2 = Book(BookType.ROMANCE, "Pride and Prejudice", date(1813, 2, 13).isoformat())
    book3 = Book(BookType.SATIRE, "Animal Farm", None)
    return [book1, book2, book3]

global books
books = set_books()

def get_books():
    return books

# Returns “No implementation for GET method”
@app.route("/v1/books/manipulation/", methods = ['GET'])
def get_book_manipulation ():
        return "No implementation for GET method"

def validateObject(bookObject):
    if "_book_type" in bookObject and "_title" in bookObject and "_creation_date" in bookObject:
        listEnumValues = [e.value for e in BookType]
        logging.info("Book type: "+str(bookObject["_book_type"]))
        if str(bookObject["_book_type"]) in listEnumValues:
            if len(bookObject["_title"]) < 256 and len(bookObject["_title"])>0:
                logging.info("Input data has valid book type and valid title")
                try:
                    date.fromisoformat(bookObject["_creation_date"])
                except:
                    logging.error("Input data has incorrect creation date")
                    return False
                return True
            else:
                logging.error("Title is more than 256 symbols or empty")
                return False
        else:
            logging.error("Book type is out of available values:"+str(listEnumValues))
            return False
    else:
        logging.error("Input data doesn't contain obligatory property")
        return False

# Add book with no arguments but request payload as json contains fields (type, title, creation date)
@app.route("/v1/books/manipulation/", methods = ['POST'])
def post_book_manipulation():
    request_data = request.get_json()
    logging.info("Data from request: " + str(request_data))
    if validateObject(request_data):
        book = Book(request_data["_book_type"], request_data["_title"], request_data["_creation_date"])
        logging.info("Book to be posted: " + str(book.json()))
        books.append(book)
        return make_response(book.json(), 201)
    else:
        return "Incorrect input data", 400

# Change the name of the book with arguments (id)
@app.route("/v1/books/manipulation/<string:id>", methods = ['PUT'])
def update_book_manipulation_by_id (id):
    request_data = request.get_json()
    logging.info("Data from request: "+str(request_data))
    if validateObject(request_data):
        for book in books:
            if book._id == id:
                logging.info("Book with id {} already exists".format(id))
                book._book_type = request_data["_book_type"]
                book._title = request_data["_title"]
                book._creation_date = request_data["_creation_date"]
                book._updated_date_time = datetime.now().isoformat()
                return make_response(book.json(), 200)

        book = Book(request_data["_book_type"], request_data["_title"], request_data["_creation_date"])
        logging.info("Book to be posted: "+str(book.json()))
        return make_response(book.json(), 201)
    else:
        return "Incorrect input data", 400

# Delete book with arguments (id)
@app.route("/v1/books/manipulation/<string:id>", methods = ['DELETE'])
def delete(id):
        for book in books:
            if book._id == id:
                books.remove(book)
                logging.info("Book was deleted " + str(book.json()))
                return "Book with id {} was deleted".format(id), 200
        return "Book with id {} was not found".format(id), 404

# Get all the latest added books limited by some amount with arguments (limit)
@app.route("/v1/books/latest/<int:limit>", methods = ['GET'])
def get_last_books (limit):
    """Get all the latest added books limited by some amount with arguments (limit)"""
    books.sort(key=lambda x: x._updated_date_time, reverse=True)
    new_books = []
    for i in range(len(books) if len(books) < limit else limit):
            new_books.append(books[i])

    return make_response(jsonify([book.json() for book in new_books]), 200)

@app.route("/v1/books/info/<string:id>", methods = ['GET'])
def get_book_by_id (id):
        """Get info about a book with arguments (ID)"""
        for book in books:
            if book._id == id:
                return make_response(jsonify(book.json()), 200)
        return "Book is not found", 404

@app.route("/v1/books/ids/<string:title>", methods = ['GET'])
def get_all_ids_for_books_with_title (title):
        """Get all ID of books by title with arguments (title)"""
        list_with_ids = []
        for book in books:
            if book._title == title:
                list_with_ids.append(book._id)

        if len(list_with_ids) == 0:
            return make_response("No books with title "+title, 404)
        return make_response(jsonify(list_with_ids), 200)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(port=5000, debug=True)

