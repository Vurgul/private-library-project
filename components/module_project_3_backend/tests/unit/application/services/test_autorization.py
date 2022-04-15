import pytest
from private_library.application import errors
from private_library.application.services import Authorization
from unittest.mock import Mock

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


def test_get_user_info(service, user_repo, user_1):
    user = service.get_user_info(user_id=1)
    assert user == user_1


def test_authentication(service, user_repo, user_1):
    user_repo = service.authentication(user_1.login, user_1.password)
    assert user_repo == user_1


def test_no_user_in_database(service, user_1):
    service.user_repo.get_by_id = Mock(return_value=None)
    with pytest.raises(errors.NoUser):
        service.get_user_info(user_id=1)


def test_unique_login(service, user_3):
    service.user_repo.get_by_login = Mock(return_value=user_3)
    with pytest.raises(errors.NotUniqueLogin):
        service.add_user(**data_user)


def test_incorrect_data(service, user_1):
    service.user_repo.get_by_user_data = Mock(return_value=None)
    with pytest.raises(errors.IncorrectData):
        service.authentication(user_1.login, user_1.password)
