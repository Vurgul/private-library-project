from unittest.mock import Mock

import pytest
from falcon import testing
from private_library.adapters import private_library_api
from private_library.application import services


@pytest.fixture(scope='function')
def library_service():
    service = Mock(services.Library)
    return service


@pytest.fixture(scope='function')
def authorization_service(user_1):
    service = Mock(services.Authorization)
    service.authentication = Mock(return_value=user_1)
    return service


@pytest.fixture(scope='function')
def client(
    library_service,
    authorization_service
):
    app = private_library_api.create_app(
        #is_dev_mode=True,
        #allow_origins='*',
        library=library_service,
        authorization=authorization_service,
    )

    return testing.TestClient(app)
