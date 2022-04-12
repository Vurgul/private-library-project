import pytest
from user_service.application import dataclasses


@pytest.fixture(scope='function')
def user_1():
    return dataclasses.User(
        id=1,
        name='test1',
        age=1
    )


@pytest.fixture(scope='function')
def user_2():
    return dataclasses.User(
        id=2,
        name='test2',
        age=1
    )
