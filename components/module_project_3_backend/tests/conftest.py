import pytest
from private_library.application import dataclasses
from datetime import datetime, timedelta


@pytest.fixture(scope='function')
def user_1():
    return dataclasses.User(
        id=1,
        name='test_name_1',
        age=1,
        login='test_login_1',
        password='test_password_1'
    )


@pytest.fixture(scope='function')
def user_2():
    return dataclasses.User(
        id=2,
        name='test_name_2',
        age=2,
        login='test_login_2',
        password='test_password_2'
    )


@pytest.fixture(scope='function')
def user_3():
    return dataclasses.User(
        id=3,
        name='test_name_3',
        age=3,
        login='test_login_3',
        password='test_password_3'
    )


@pytest.fixture(scope='function')
def book_1():
    return dataclasses.Book(
        id=1,
        title="test_title_1",
        subtitle="test_subtitle_1",
        authors="test_authors_1",
        publisher="test_publisher_1",
        language="test_language_1",
        isbn13="test_isbn13_1",
        pages=100,
        year=2001,
        rating=1.0,
        desc="test_desc_1",
        price_USD=11.1,
        tag="test_tag_1"
    )


@pytest.fixture(scope='function')
def book_2():
    return dataclasses.Book(
        id=2,
        title="test_title_2",
        subtitle="test_subtitle_2",
        authors="test_authors_2",
        publisher="test_publisher_2",
        language="test_language_2",
        isbn13="test_isbn13_2",
        pages=200,
        year=2002,
        rating=2.0,
        desc="test_desc_2",
        price_USD=12.2,
        tag="test_tag_2"
    )


@pytest.fixture(scope='function')
def book_3():
    return dataclasses.Book(
        id=3,
        title="test_title_3",
        subtitle="test_subtitle_3",
        authors="test_authors_3",
        publisher="test_publisher_3",
        language="test_language_3",
        isbn13="test_isbn13_3",
        pages=300,
        year=2003,
        rating=3.0,
        desc="test_desc_3",
        price_USD=13.3,
        tag="test_tag_3"
    )


@pytest.fixture(scope='function')
def journal_1():
    return dataclasses.Journal(
        id=1,
        user_id=1,
        book_id=1,
        status='return',
        taking_date=datetime(2021, 4, 15, 10, 0, 0),
        timedelta=timedelta(days=7),
        returning_date=datetime(2021, 4, 15, 11, 0, 0)
    )


@pytest.fixture(scope='function')
def journal_2():
    return dataclasses.Journal(
        id=2,
        user_id=1,
        book_id=2,
        status='take',
        taking_date=datetime(2021, 4, 15, 12, 0, 0),
        timedelta=timedelta(days=7),
        returning_date=None
    )


@pytest.fixture(scope='function')
def journal_3():
    return dataclasses.Journal(
        id=3,
        user_id=2,
        book_id=3,
        status='buy',
        taking_date=datetime(2021, 4, 15, 12, 0, 0),
        timedelta=timedelta(days=7),
        returning_date=None
    )
