from unittest.mock import Mock

import pytest
from falcon import testing
from user_service.adapters import user_api
from user_service.application import services


@pytest.fixture(scope='function')
def users_service():
    service = Mock(services.UserService)

    return service


@pytest.fixture(scope='function')
def client(
    users_service,
):
    app = user_api.create_app(
        #is_dev_mode=True,
        #allow_origins='*',
        users=users_service,
    )

    return testing.TestClient(app)
