import logging

import pytest

from hamcrest import assert_that, equal_to
from requests import get, post, put, delete

server_url = "http://127.0.0.1"
server_host = "5000"

def setup_module():
    logging.basicConfig(level=logging.INFO)
    logging.info("module setup")

def teardown_module():
    logging.info("module teardown")

@pytest.mark.post
@pytest.mark.smoke
@pytest.mark.positive
def test_create_book_with_valid_data_return_201():
    new_book = {
        "_book_type":"Romance",
        "_title":"Bridget Jones's Diary",
        "_creation_date":"1996-01-12"
    }
    url_for_create_book = server_url+":"+server_host+"/v1/books/manipulation/"
    response = post(url_for_create_book, json=new_book)

    assert_that(response.status_code, equal_to( 201))
    assert_that(response.json()["_title"] == "Bridget Jones's Diary")
    assert_that(response.json()["_book_type"] == "Romance")
    assert_that(response.json()["_creation_date"] == "1996-01-12")

@pytest.mark.post
@pytest.mark.smoke
@pytest.mark.negative
def test_create_book_with_invalid_quantity_of_parameters_return_400():
    new_book = {
        "_book_type": "Romance",
        "_creation_date": "1996-01-12"
    }
    url_for_create_book = server_url + ":" + server_host + "/v1/books/manipulation/"
    response = post(url_for_create_book, json=new_book)

    assert_that( response.status_code, equal_to( 400))
    assert_that( str(response.reason), equal_to("BAD REQUEST" ))
    assert_that( response.text == "Incorrect input data" )

@pytest.mark.post
@pytest.mark.smoke
@pytest.mark.negative
def test_create_book_with_invalid_value_of_title_return_400():
    incorrect_title = """pANCaQ6RV8xKZRJpMVeh46WX31eTOPf8sb2lOztKYygCT57uFEg472Dotp3OlvAEuZ6FeSPfoE5iYZESkpg0imiO69
                        NLBRNw0FiNdoTQ0eGeVSPYhbRAc6eLXYPeeirnmvEZP3dsiei7zrS9GRplvlVWvhQyzHwy9YHbfayZvK083yfQG3UfTC
                        JazmckgUzrtlA6GTHstHp0AoHJLo8ld6NnEtCQcbDdJR3XYp5NR4fNPOoZ3Ku9hiLeRD7boLe13""";
    new_book = {"_book_type": "Romance",
                "_title":incorrect_title,
                "_creation_date": "1996-01-12"
                }
    url_for_create_book = server_url + ":" + server_host + "/v1/books/manipulation/"
    response = post(url_for_create_book, json=new_book)

    assert_that( response.status_code, equal_to( 400 ))
    assert_that( response.reason == "BAD REQUEST" )
    assert_that( response.text == "Incorrect input data" )

@pytest.mark.get
@pytest.mark.smoke
@pytest.mark.positive
def test_get_last_book():
    #Pre-condition
    new_book = {"_book_type": "Science Fiction",
                "_title": "Brave New World",
                "_creation_date": "1932-01-12"
                }
    url_for_create_book = server_url + ":" + server_host + "/v1/books/manipulation/"
    logging.info("URl for post is :"+url_for_create_book)
    response = post(url_for_create_book, json=new_book)
    assert response.status_code == 201

    #Main part
    limit=1
    url = server_url+":"+server_host+"/v1/books/latest/" + str(limit)
    response = get(url)
    logging.info("URl for GET request is :" + url)
    assert_that (response.status_code, equal_to( 200))
    assert_that(response.json()[0]["_title"], equal_to( "Brave New World"))

@pytest.mark.get
@pytest.mark.smoke
@pytest.mark.positive
def test_get_manipulation_book_has_valid_response_message():
    url = server_url + ":" + server_host + "/v1/books/manipulation/"
    response = get(url)
    assert_that( response.status_code, equal_to( 200) )
    assert_that( response.text, "No implementation for GET method")

@pytest.mark.get
@pytest.mark.smoke
@pytest.mark.positive
def test_get_ids_for_book_with_exist_title_return_200():
    #Pre-condition
    new_book = {"_book_type": "Drama",
                "_title": "The Hunger Games",
                "_creation_date": "2008-01-12"
                }
    url_for_create_book = server_url + ":" + server_host + "/v1/books/manipulation/"
    logging.info("URl for post is :"+url_for_create_book)
    response = post(url_for_create_book, json=new_book)
    assert response.status_code == 201

    #Main part
    expected_id = response.json()["_id"]
    title = response.json()["_title"]
    url = server_url + ":" + server_host + "/v1/books/ids/{}".format(title)
    logging.info("URl for GET is :" + url)
    response = get(url)

    assert_that(response.status_code, equal_to( 200))
    assert_that(expected_id in response.json())

@pytest.mark.put
@pytest.mark.smoke
@pytest.mark.positive
def test_update_existed_book_with_valid_data_return_200():
    #Pre-condition
    new_book = {"_book_type": "Drama",
                "_title": "The Hunger Games",
                "_creation_date": "2008-01-12"
                }
    url_for_create_book = server_url + ":" + server_host + "/v1/books/manipulation/"
    logging.info("URl for post is :" + url_for_create_book)
    response = post(url_for_create_book, json=new_book)
    assert response.status_code == 201

    #Main part
    id = response.json()["_id"]
    changed_book = new_book
    changed_book["_book_type"]= "Action and Adventure"
    url_for_update_book = server_url + ":" + server_host + "/v1/books/manipulation/{}".format(id)
    logging.info("URl for PUT is :" + url_for_update_book)
    response = put(url_for_update_book, json=changed_book)
    assert_that(response.status_code, equal_to(200))
    assert_that(response.json()["_book_type"], equal_to(changed_book["_book_type"]))

@pytest.mark.put
@pytest.mark.smoke
@pytest.mark.negative
def test_update_existed_book_with_invalid_data_return_400():
    #Pre-condition
    new_book = {"_book_type": "Drama",
                "_title": "The Hunger Games",
                "_creation_date": "2008-01-12"
                }
    url_for_create_book = server_url + ":" + server_host + "/v1/books/manipulation/"
    logging.info("URl for post is :"+url_for_create_book)
    response = post(url_for_create_book, json=new_book)
    assert response.status_code == 201

    #Main part
    id = response.json()["_id"]
    changed_book = new_book
    changed_book["_book_type"]= "Action"
    url_for_update_book = server_url + ":" + server_host + "/v1/books/manipulation/{}".format(id)
    logging.info("URl for PUT is :"+url_for_update_book)
    response = put(url_for_update_book, json=changed_book)
    assert_that(response.status_code, equal_to(400))

@pytest.mark.put
@pytest.mark.smoke
@pytest.mark.positive
def test_update_non_existed_book_return_201():
    book = {
        "_book_type": "Drama",
        "_title": "The Hunger Games",
        "_creation_date": "2008-01-12"
    }
    url_for_update_book = server_url + ":" + server_host + "/v1/books/manipulation/{}".format("non_existing_id")
    logging.info("URl for post is :"+url_for_update_book)
    response = put(url_for_update_book, json=book)

    assert_that(response.status_code, equal_to(201))
    assert_that(response.json()["_title"], equal_to("The Hunger Games"))
    assert_that(response.json()["_book_type"], equal_to("Drama"))
    assert_that(response.json()["_creation_date"], equal_to("2008-01-12"))

@pytest.mark.delete
@pytest.mark.smoke
@pytest.mark.positive
def test_delete_existed_book_return_200():
    #Pre-condition
    new_book = {"_book_type": "Drama",
                "_title": "The Hunger Games",
                "_creation_date": "2008-01-12"
                }
    url_for_create_book = server_url + ":" + server_host + "/v1/books/manipulation/"
    logging.info("URl for post is :"+url_for_create_book)
    response = post(url_for_create_book, json=new_book)
    assert response.status_code == 201

    #Main part
    id = response.json()["_id"]
    url_for_book_deletion = server_url + ":" + server_host + "/v1/books/manipulation/{}".format(id)
    logging.info("URl for DELETE is :" + url_for_book_deletion)
    response = delete(url_for_book_deletion)
    assert_that(response.status_code, equal_to(200))

@pytest.mark.delete
@pytest.mark.smoke
@pytest.mark.negative
def test_delete_non_existed_book_return_404():
    url_for_book_deletion = server_url + ":" + server_host + "/v1/books/manipulation/{}".format("non_existing_id")
    logging.info("URl for DELETE is :" + url_for_book_deletion)
    response = delete(url_for_book_deletion)

    assert_that(response.status_code, equal_to(404))
    assert_that(response.reason, equal_to("NOT FOUND"))

@pytest.mark.get
@pytest.mark.smoke
@pytest.mark.positive
def test_get_book_by_existing_id_return_200():
    #Pre-condition
    new_book = {"_book_type": "Drama",
                "_title": "Twilight",
                "_creation_date": "2005-01-12"
                }
    url_for_create_book = server_url + ":" + server_host + "/v1/books/manipulation/"
    logging.info("URl for post is :"+url_for_create_book)
    response = post(url_for_create_book, json=new_book)
    assert response.status_code == 201

    #Main part
    id= response.json()["_id"]
    url = server_url + ":" + server_host + "/v1/books/info/{}".format(id)
    logging.info("URl for GET is :" + url)
    response = get(url)

    assert_that(response.status_code, equal_to( 200))
    assert_that(response.json()["_title"] == "Twilight")
    assert_that(response.json()["_book_type"] == "Drama")
    assert_that(response.json()["_creation_date"] == "2005-01-12")

@pytest.mark.get
@pytest.mark.smoke
@pytest.mark.negative
def test_get_book_by_non_existing_id_return_404():
    id = "invalid_id"
    url = server_url + ":" + server_host + "/v1/books/info/{}".format(id)
    response = get(url)
    logging.info("URl for GET is :" + url)

    assert_that(response.status_code, equal_to(404))

#Parametrized test
@pytest.fixture(scope="function", params=[
    ("Science Fiction", 201),
    ("Satire", 201),
    ("Drama", 201),
    ("Action and Adventure", 201),
    ("Romance", 201),
    ("Incorrect type", 400)],
                ids=["Valid book type 'Science Fiction'",
                     "Valid book type 'Satire'",
                     "Valid book type 'Drama'",
                     "Valid book type 'Action and Adventure'",
                     "Valid book type 'Romance'",
                     "Invalid book type"])
def param_test(request):
    return request.param

def test_book_type_values(param_test):
    (book_type, expected_status_code) = param_test
    new_book = {
        "_book_type":book_type,
        "_title":"book type test",
        "_creation_date":"1990-01-12"
    }
    url_for_create_book = server_url+":"+server_host+"/v1/books/manipulation/"
    response = post(url_for_create_book, json=new_book)

    assert_that(response.status_code, equal_to( expected_status_code))




