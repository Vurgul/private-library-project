from unittest.mock import Mock

import pytest
from private_library.application import errors
from private_library.application.services import Library

data_filter = {
    'price_USD': '10',
    'keyword': 'test',
    'publisher': 'test',
    'order_by': 'test',
}


@pytest.fixture(scope='function')
def service(book_repo, user_repo, journal_repo):
    return Library(
        book_repo=book_repo, user_repo=user_repo, journal_repo=journal_repo
    )


def test_take_users_info(service, user_1, user_2):
    users = service.take_users_info()
    assert isinstance(users, list)
    assert user_1 in users
    assert user_2 in users
    assert len(users) == 2


def test_take_books_info(service, book_1, book_2, book_3):
    books = service.take_books_info()
    assert isinstance(books, list)
    assert book_1 in books
    assert book_2 in books
    assert book_3 in books
    assert len(books) == 3


def test_take_books_with_filter_and_sort(service):
    service.take_books_with_filter_and_sort(**data_filter)
    service.book_repo.get_query.assert_called_once()
    service.book_repo.filter_by_price.assert_called_once()
    service.book_repo.filter_by_publisher.assert_called_once()
    service.book_repo.filter_by_keyword.assert_called_once()
    service.book_repo.order_by.assert_called_once()
    service.book_repo.get_filter_data.assert_called_once()

    service.book_repo.filter_by_authors.assert_not_called()


def test_take_book_info(service, book_1):
    book = service.take_book_info(book_1.id)
    assert book == book_1


def test_take_self_journal(service, user_1, journal_2):
    journal_records = service.take_self_journal(user_1.id)
    assert journal_2 in journal_records


def test_take_active_book(service, user_1, book_1):
    book = service.take_active_book(user_1.id)
    service.book_repo.get_by_id.assert_called_once()
    assert book.id == book_1.id


def test_open_reserve_book(service, user_2, book_1, journal_1):
    service.journal_repo.get_by_user_id = Mock(return_value=[journal_1])

    service.journal_repo.get_by_book_id = Mock(return_value=[journal_1])
    service.open_reserve_book(user_2.id, book_1.id)
    service.journal_repo.add.assert_called_once()

    service.journal_repo.get_by_book_id = Mock(return_value=[])
    service.open_reserve_book(user_2.id, book_1.id)
    service.journal_repo.add.assert_called()

    service.open_reserve_book(user_2.id, book_1.id, 10)
    service.journal_repo.add.assert_called()


def test_create_journal_record(service, user_1, book_1):
    service.create_journal_record(
        user_id=user_1.id, book_id=book_1.id, status='take'
    )
    service.journal_repo.add.assert_called_once()


def test_close_reserve_book(service, user_1):
    service.close_reserve_book(user_1.id)
    service.journal_repo.get_active_record.assert_called_once()


def test_buy_book(service, user_1):
    service.buy_book(user_1.id)
    service.journal_repo.get_active_record.assert_called_once()


def test_no_user_in_database(service, user_1, book_1):
    service.book_repo.get_by_id = Mock(return_value=None)
    with pytest.raises(errors.NoBook):
        service.take_book_info(book_id=1)
        service.take_active_book(user_1.id)
        service.open_reserve_book(user_1.id, book_1.id)


def test_no_journal_record(service, user_1):
    service.journal_repo.get_active_record = Mock(return_value=None)
    with pytest.raises(errors.NoJournal):
        service.take_active_book(user_1.id)
        service.buy_book(user_1.id)
        service.create_journal_record(user_1.id)


def test_user_have_active_book(service, user_1, book_1, journal_2):
    service.journal_repo.get_by_user_id = Mock(return_value=[journal_2])
    with pytest.raises(errors.HaveActiveBook):
        service.open_reserve_book(user_1.id, book_1.id)


def test_book_busy(service, user_1, book_1, journal_2):
    service.journal_repo.get_by_user_id = Mock(return_value=[])
    service.journal_repo.get_by_book_id = Mock(return_value=[journal_2])
    with pytest.raises(errors.BookBusy):
        service.open_reserve_book(user_1.id, book_1.id)


def test_book_buy(service, user_1, book_1, journal_3):
    service.journal_repo.get_by_user_id = Mock(return_value=[])
    service.journal_repo.get_by_book_id = Mock(return_value=[journal_3])
    with pytest.raises(errors.BookBuy):
        service.open_reserve_book(user_1.id, book_1.id)
