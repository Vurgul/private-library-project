from unittest.mock import Mock

import pytest
from private_library.application import interfaces


@pytest.fixture(scope='function')
def user_repo(user_1, user_2):
    user_repo = Mock(interfaces.UsersRepo)
    user_repo.get_by_id = Mock(return_value=user_1)
    user_repo.get_by_login = Mock(return_value=None)
    user_repo.get_by_user_data = Mock(return_value=user_1)
    user_repo.get_all = Mock(return_value=[user_1, user_2])
    return user_repo


@pytest.fixture(scope='function')
def book_repo(book_1, book_2, book_3):
    book_repo = Mock(interfaces.BooksRepo)
    book_repo.get_by_id = Mock(return_value=book_1)
    book_repo.get_all = Mock(return_value=[book_1, book_2, book_3])
    return book_repo


@pytest.fixture(scope='function')
def journal_repo(journal_1, journal_2, journal_3):
    journal_repo = Mock(interfaces.BooksRepo)
    journal_repo.get_by_id = Mock(return_value=journal_2)
    journal_repo.get_all = Mock(return_value=[journal_1, journal_2, journal_3])
    return journal_repo
