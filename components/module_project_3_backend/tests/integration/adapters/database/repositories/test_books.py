import pytest
from private_library.adapters.database import tables
from private_library.adapters.database.repositories import BooksRepo


@pytest.fixture(scope='function')
def fill_db_books(session):
    books_data = [
        {
            'id': 1,
            'title': 'test_title_1',
            'subtitle': 'test_subtitle_1',
            'authors': 'test_authors_1',
            'publisher': 'test_publisher_1',
            'language': 'test_language_1',
            'isbn13': 'test_isbn13_1',
            'pages': 300,
            'year': 2003,
            'rating': 3.0,
            'desc': 'test_desc_1',
            'price_USD': 13.3,
            'tag': 'test_tag_1'
        },
        {
            'id': 2,
            'title': 'test_title_2',
            'subtitle': 'test_subtitle_2',
            'authors': 'test_authors_2',
            'publisher': 'test_publisher_2',
            'language': 'test_language_2',
            'isbn13': 'test_isbn13_2',
            'pages': 30,
            'year': 2003,
            'rating': 3.0,
            'desc': 'test_desc_2',
            'price_USD': 1.3,
            'tag': 'test_tag_2'
        }
    ]

    session.execute(tables.books.insert(), books_data)


@pytest.fixture(scope='function')
def repo(transaction_context):
    return BooksRepo(context=transaction_context)


def test_get_by_id(repo, fill_db_books):
    result = repo.get_by_id(id=1)
    assert result.id == 1


def test_add(repo, session, book_3):
    initial_data = session.execute(tables.books.select()).all()
    assert len(initial_data) == 0

    repo.add(book_3)

    data = session.execute(tables.books.select()).all()
    assert len(data) == 1


def test_get_all(repo, fill_db_books):
    result = repo.get_all()
    assert len(result) == 2


def test_get_by_isbn13(repo, fill_db_books):
    result = repo.get_by_isbn13(isbn13='test_isbn13_2')
    assert result.id == 2


def test_get_query(repo, fill_db_books, session):
    query = repo.get_query()
    assert isinstance(query, object)


def test_get_filter_data(repo, fill_db_books, session):
    query = repo.get_query()
    result = repo.get_filter_data(query)
    assert len(result) == 2


def test_filter_by_price(repo, fill_db_books, session):
    prices = ['10', 'efw', 'gte:1', 'lte:1']

    query = repo.get_query()

    queries = [repo.filter_by_price(price, query) for price in prices]
    results = [repo.get_filter_data(query) for query in queries]

    assert list(map(len, results)) == [1, 2, 2, 0]


def test_filter_by_authors(repo, fill_db_books, session):
    authors_like = ['test_authors_1', 'test_authors_', 'test_', '122']

    query = repo.get_query()

    queries = [repo.filter_by_authors(author, query) for author in authors_like]
    results = [repo.get_filter_data(query) for query in queries]

    assert list(map(len, results)) == [1, 2, 2, 0]


def test_filter_by_publisher(repo, fill_db_books, session):
    publisher_like = ['test_publisher_1', 'test_publisher_', 'test_', '122']

    query = repo.get_query()

    queries = [
        repo.filter_by_publisher(
            publisher,
            query
        ) for publisher in publisher_like
    ]
    results = [repo.get_filter_data(query) for query in queries]

    assert list(map(len, results)) == [1, 2, 2, 0]


def test_order_by(repo, fill_db_books, session):
    orders_by = ['price_USD', 'pages', 'test_']

    query = repo.get_query()

    queries = [repo.order_by(order, query) for order in orders_by]
    results = [repo.get_filter_data(query) for query in queries]

    assert list(map(len, results)) == [2, 2, 2]
    assert results[0][0].id == 2
    assert results[1][0].id == 2
    assert results[2][0].id == 1


def test_get_top_three(repo, fill_db_books, session):
    result = repo.get_top_three('test_tag_2')
    assert len(result) == 1
