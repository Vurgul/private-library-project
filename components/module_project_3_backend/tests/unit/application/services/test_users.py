from unittest.mock import Mock

import pytest
from user_service.application import errors
from user_service.application.services import UserService

data_user = {
    'id': 3,
    'name': 'test3',
    'age': 3
}

data_user_update = {
    'user_id': 1,
    'name': 'NewName',
}


@pytest.fixture(scope='function')
def service(user_repo):
    return UserService(user_repo=user_repo, publisher=None)


def test_get_user_info(service, user_repo, user_1):
    user = service.get_user_info(user_id=user_1.id)
    assert user == user_1


def test_get_users_info(service, user_1, user_2):
    users = service.get_users_info()
    assert user_1 in users
    assert user_2 in users
    assert len(users) == 2


def test_create_user(service):
    service.create_user(**data_user)
    service.user_repo.add.assert_called_once()


def test_update_user_info(service, user_1):
    service.update_user_info(**data_user_update)
    assert user_1.name == 'NewName'
    assert user_1.age == 1


def test_delete_user(service, user_1):
    service.delete_user(user_id=user_1.id)
    service.user_repo.remove.assert_called_once()


def test_no_user_in_database(service, user_1):
    service.user_repo.get_by_id = Mock(return_value=None)
    with pytest.raises(errors.NoUser):
        service.get_user_info(user_id=10)
        service.update_user_info(**data_user_update)
        service.delete_user(user_id=user_1.id)
