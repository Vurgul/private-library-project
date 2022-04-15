import pytest
from private_library.application import errors
from private_library.application.services import BookServices
from unittest.mock import Mock

data_book = {
    'id': 3,
    'title': 'test_title_3',
    'subtitle': "test_subtitle_3",
    'authors': "test_authors_3",
    'publisher': "test_publisher_3",
    'language': "test_language_3",
    'isbn13': "test_isbn13_3",
    'pages': 300,
    'year': 2003,
    'rating': 3.0,
    'desc': "test_desc_3",
    'price_USD': 13.3,
    'tag': "test_tag_3"
}


@pytest.fixture(scope='function')
def service(book_repo):
    return BookServices(book_repo=book_repo)


def test_add_book(service):
    #service.add_book
    pass
