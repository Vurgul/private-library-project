import pytest

from private_library.adapters.database import tables
from private_library.adapters.database.repositories import UsersRepo


@pytest.fixture(scope='function')
def fill_db_users(session):
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

    session.execute(tables.users.insert(), users_data)


@pytest.fixture(scope='function')
def repo(transaction_context):
    return UsersRepo(context=transaction_context)


def test_get_by_id(repo, fill_db_users):
    result = repo.get_by_id(id=1)
    assert result.id == 1


def test_add(repo, session, user_3):
    initial_data = session.execute(tables.users.select()).all()
    assert len(initial_data) == 0

    repo.add(user_3)

    data = session.execute(tables.users.select()).all()
    assert len(data) == 1


def test_get_all(repo, fill_db_users):
    result = repo.get_all()
    assert len(result) == 2


def test_get_by_user_data(repo, fill_db_users):
    result = repo.get_by_user_data(
        login='test_login_2',
        password='test_password_2'
    )
    assert result.id == 2


def test_get_by_login(repo, fill_db_users):
    result = repo.get_by_login(login='test_login_1')
    assert result.id == 1
