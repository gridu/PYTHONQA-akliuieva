<h3>Task: Create a REST service</h3>
<p>

**Common requirements:** <br>

As a QA I want to manage by a catalog of books. <br>
The following information about a book should be stored:<br>

1. Type:
    * Science Fiction
    * Satire
    * Drama
    * Action and Adventure
    * Romance
1. Title(String(length<256 symbols))
1. ID(String) (should be unique, uuid4)
1. Creation date (YYYY-MM-DD) (can be null)
1. Updated date time (ISO 8601)

**The following methods should be implemented:**

1. `/v1/books/manipulation` POST - Add book with no arguments but request payload as json contains fields  (type, title, creation date)
2. `/v1/books/manipulation` DELETE - Delete book with arguments (id)
3. `/v1/books/manipulation` PUT - Change the name of the book with arguments (id) (NOTE: updated time should be changed as well)
4. `/v1/books/manipulation` GET - Returns “No implementation for `GET` method”
5. `/v1/books/latest` GET - Get all the latest added books limited by some amount with arguments (limit)
6. `/v1/books/info` GET - Get info(type, name etc …) about a book with arguments (ID)
7. `/v1/books/ids` GET - Get all ID of books by title with arguments (title)

**Technical requirements:**

* Python3 should be used. (python3 your_script.py). A virtual environment should be used to run it.
* Content-type: application/json.
* There is no need to use some database, all data can be stored in variables in the process. It’s ok to lose all data when the service will be down.
* For storing types enum should be used.
* The script should be supported by requirenements.txt
* Logging should be used.
* `__main__` block should be used for the main block.
</p>

**How to run:**

On Unix or MacOS, run:

`python3 -m venv restService-env` 
<br>
`source restService-env/bin/activate`

Install required packages:
`pip3 install -r requirements.txt`

Run rest service:
`python3 restService/BookService.py`

Run tests:
`pytest tests/BookServiceTest.py`

Run smoke tests:
`pytest -v -m "smoke" tests/BookServiceTest.py`

Run smoke tests or get tests:
`pytest -v -m "smoke or get" tests/BookServiceTest.py`
