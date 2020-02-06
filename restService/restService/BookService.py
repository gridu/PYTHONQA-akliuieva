#!/usr/bin/env python3
from flask import Flask, jsonify, make_response, request
from datetime import date, datetime
import logging
import configparser

from Book import Book, BookType

app = Flask(__name__)  # “__name__” is a Python special variable which gives Python file a unique name


def set_books():
    book1 = Book(BookType.ACTION_AND_ADVENTURE, "The Fountainhead", date(1943, 10, 1).isoformat())
    book2 = Book(BookType.ROMANCE, "Pride and Prejudice", date(1813, 2, 13).isoformat())
    book3 = Book(BookType.SATIRE, "Animal Farm", None)
    return [book1, book2, book3]


global books
books = set_books()


def is_book_type_has_valid_value(income_book_type):
    list_enum_values = [e.value for e in BookType]
    logging.info("Book type: " + str(income_book_type))
    if str(income_book_type) in list_enum_values:
        return True
    else:
        logging.error("Book type is out of available values:" + str(list_enum_values))
        return False


def is_title_has_valid_lengths(income_title):
    if 256 > len(income_title) > 0:
        logging.info("Input data has valid book type and valid title")
        return True
    else:
        logging.error("Title is more than 256 symbols or empty")
        return False


def is_date_has_valid_format(income_date):
    try:
        date.fromisoformat(income_date)
    except:
        logging.error("Input data has incorrect creation date")
        return False
    return True


def has_correct_values(income_data):
    if is_book_type_has_valid_value(income_data["_book_type"]) and is_title_has_valid_lengths(
            income_data["_title"]) and is_date_has_valid_format(income_data["_creation_date"]):
        return True
    else:
        return False


def validate_object(bookObject):
    if "_book_type" in bookObject and "_title" in bookObject and "_creation_date" in bookObject:
        return has_correct_values(bookObject)
    else:
        logging.error("Input data doesn't contain obligatory property")
    return False


@app.route("/v1/books/manipulation/", methods=['GET'])
def get_book_manipulation():
    """Stub method that that returns "No implementation for GET method"
        Args:
            no args

        Return:
            "No implementation for GET method" string
        """
    return "No implementation for GET method"


@app.route("/v1/books/manipulation/", methods=['POST'])
def post_book_manipulation():
    """Create new book with income data
        Args:
            no args

        Return:
            Json with new book
        """
    request_data = request.get_json()
    logging.info("Data from request: " + str(request_data))
    if validate_object(request_data):
        book = Book(request_data["_book_type"], request_data["_title"], request_data["_creation_date"])
        logging.info("Book to be posted: " + str(book.json()))
        books.append(book)
        return make_response(book.json(), 201)
    else:
        return "Incorrect input data", 400


@app.route("/v1/books/manipulation/<string:id>", methods=['PUT'])
def update_book_manipulation_by_id(id):
    """Update the book with income data
    Args:
        id:(string) The id of the book

    Return:
        Json with updated data
    """
    request_data = request.get_json()
    logging.info("Data from request: " + str(request_data))
    if validate_object(request_data):
        for book in books:
            if book._id == id:
                logging.info("Book with id {} already exists".format(id))
                book._book_type = request_data["_book_type"]
                book._title = request_data["_title"]
                book._creation_date = request_data["_creation_date"]
                book._updated_date_time = datetime.now().isoformat()
                return make_response(book.json(), 200)

        book = Book(request_data["_book_type"], request_data["_title"], request_data["_creation_date"])
        logging.info("Book to be posted: " + str(book.json()))
        return make_response(book.json(), 201)
    else:
        return "Incorrect input data", 400


@app.route("/v1/books/manipulation/<string:id>", methods=['DELETE'])
def delete(id):
    """Delete the book with specific id
    Args:
        id:(string) The id of the book

    Return:
        Response status equals to 200 if  the book was deleted successfully
        Response status equals to 404 if the book was non deleted
    """
    for book in books:
        if book._id == id:
            books.remove(book)
            logging.info("Book was deleted " + str(book.json()))
            return "Book with id {} was deleted".format(id), 200
    return "Book with id {} was not found".format(id), 404


@app.route("/v1/books/latest/<int:limit>", methods=['GET'])
def get_last_books(limit):
    """Get all the latest added books limited by some amount with arguments (limit)
    Args:
        limit:(int) The quantity of the latest added books

    Return:
        Json with list of books
    """
    books.sort(key=lambda x: x._updated_date_time, reverse=True)
    result = len(books) if len(books) < limit else limit

    return make_response(jsonify([book.json() for book in books[:result]]), 200)


@app.route("/v1/books/info/<string:id>", methods=['GET'])
def get_book_by_id(id):
    """Get info about a book with arguments (ID)
    Args:
        id:(string) The id of the book

    Return:
        Json with book with id mentioned as parameter
    """
    for book in books:
        if book._id == id:
            return make_response(jsonify(book.json()), 200)
    return "Book is not found", 404


@app.route("/v1/books/ids/<string:title>", methods=['GET'])
def get_all_ids_for_books_with_title(title):
    """Get all ID of books by title with arguments (title)
    Args:
        title:(string) The title of the book

    Return:
        Json with list of books
    """
    list_with_ids = []
    for book in books:
        if book._title == title:
            list_with_ids.append(book._id)

    if not list_with_ids:
        return make_response("No books with title " + title, 404)
    return make_response(jsonify(list_with_ids), 200)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = configparser.ConfigParser()
    config.read('configuration.ini')
    port_number = int(config['flask.server']['Port'])
    host = config['flask.server']['Host']
    app.run(host=host, port=port_number)
