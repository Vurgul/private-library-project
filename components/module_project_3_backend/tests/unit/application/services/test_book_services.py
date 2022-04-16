from unittest.mock import Mock

import pytest
from private_library.application.services import BookServices

data_book = {
    'id': 3,
    'title': 'test_title_3',
    'subtitle': 'test_subtitle_3',
    'authors': 'test_authors_3',
    'publisher': 'test_publisher_3',
    'language': 'test_language_3',
    'isbn13': 'test_isbn13_3',
    'pages': 300,
    'year': 2003,
    'rating': 3.0,
    'desc': 'test_desc_3',
    'price_USD': 13.3,
    'tag': 'test_tag_3'
}


@pytest.fixture(scope='function')
def service(book_repo, user_repo):
    return BookServices(
        book_repo=book_repo,
        user_repo=user_repo
    )


def test_add_book(service, book_3):
    service.add_book(**data_book)
    service.book_repo.add.assert_called_once()


def test_send_message(service, user_1, user_2):
    service.send_message('tag')
    service.user_repo.get_all.assert_called_once()
    service.book_repo.get_top_three.assert_called()
    service.book_repo.get_top_three.assert_called_with('tag')


def test_not_add_book_repeat_isbn13(service, book_1):
    service.book_repo.get_by_isbn13 = Mock(return_value=book_1)
    service.add_book(**data_book)
    service.book_repo.add.assert_not_called()

