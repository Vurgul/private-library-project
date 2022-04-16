import pytest
from datetime import datetime, timedelta
from private_library.adapters.database import tables
from private_library.adapters.database.repositories import JournalRepo


@pytest.fixture(scope='function')
def fill_db(session):
    users_data = [
        {
            'id': 1,
            'name': 'test_name_1',
            'age': 1,
            'login': 'test_login_1',
            'password': 'test_password_1'
        },
        {
            'id': 2,
            'name': 'test_name_2',
            'age': 2,
            'login': 'test_login_2',
            'password': 'test_password_2',

        }
    ]

    books_data = [
        {
            'id': 1,
            'title': 'test_title_1',
            'subtitle': 'test_subtitle_1',
            'authors': 'test_authors_1',
            'publisher': 'test_publisher_1',
            'language': 'test_language_1',
            'isbn13': 'test_isbn13_1',
            'pages': 300,
            'year': 2003,
            'rating': 3.0,
            'desc': 'test_desc_1',
            'price_USD': 13.3,
            'tag': 'test_tag_1'
        },
        {
            'id': 2,
            'title': 'test_title_2',
            'subtitle': 'test_subtitle_2',
            'authors': 'test_authors_2',
            'publisher': 'test_publisher_2',
            'language': 'test_language_2',
            'isbn13': 'test_isbn13_2',
            'pages': 30,
            'year': 2003,
            'rating': 3.0,
            'desc': 'test_desc_2',
            'price_USD': 1.3,
            'tag': 'test_tag_2'
        }
    ]

    journal_data = [
        {
            'id': 1,
            'user_id': 1,
            'book_id': 1,
            'status': 'take',
            'taking_date': datetime(2021, 4, 15, 12, 0, 0),
            'timedelta': timedelta(days=7),
            'returning_date': None,
        },
        {
            'id': 2,
            'user_id': 1,
            'book_id': 2,
            'status': 'buy',
            'taking_date': datetime(2021, 4, 15, 12, 0, 0),
            'timedelta': timedelta(days=7),
            'returning_date': None,

        }
    ]

    session.execute(tables.books.insert(), books_data)
    session.execute(tables.users.insert(), users_data)
    session.execute(tables.journal.insert(), journal_data)


@pytest.fixture(scope='function')
def repo(transaction_context):
    return JournalRepo(context=transaction_context)


def test_get_by_id(repo, fill_db):
    result = repo.get_by_id(id=1)
    assert result.id == 1


def test_add(repo, session, journal_4, fill_db):
    initial_data = session.execute(tables.journal.select()).all()
    assert len(initial_data) == 2

    repo.add(journal_4)
    data = session.execute(tables.journal.select()).all()
    assert len(data) == 3


def test_get_all(repo, fill_db):
    result = repo.get_all()
    assert len(result) == 2


def test_get_by_user_id(repo, fill_db, user_1):
    result = repo.get_by_user_id(user_1.id)
    assert isinstance(result, list)
    assert result[0].id == 1


def test_get_by_book_id(repo, fill_db, book_1):
    result = repo.get_by_user_id(book_1.id)
    assert isinstance(result, list)
    assert result[0].id == 1


def test_get_active_record(repo, fill_db, user_1, user_2):
    result_one = repo.get_active_record(user_1.id)
    result_none = repo.get_active_record(user_2.id)
    assert result_one.user_id == 1
    assert result_one.status == 'take'
    assert result_none is None


