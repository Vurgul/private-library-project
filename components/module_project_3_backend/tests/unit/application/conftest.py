from unittest.mock import Mock

import pytest
from user_service.application import interfaces


@pytest.fixture(scope='function')
def user_repo(user_1, user_2):
    user_repo = Mock(interfaces.UsersRepo)
    user_repo.get_by_id = Mock(return_value=user_1)
    user_repo.get_all = Mock(return_value=[user_1, user_2])
    return user_repo

