import pytest
from private_library.application import errors
from private_library.application.services import Authorization

data_user = {
    'id': 3,
    'name': 'test_name_3',
    'age': 3,
    'login': 'test_login_3',
    'password': 'test_password_3'
}


@pytest.fixture(scope='function')
def service(user_repo):
    return Authorization(user_repo=user_repo)


def test_add_user(service):
    service.add_user(**data_user)
    service.user_repo.add.assert_called_once()

