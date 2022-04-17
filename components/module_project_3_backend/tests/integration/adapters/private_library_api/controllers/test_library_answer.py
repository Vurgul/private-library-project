from http import HTTPStatus

TEST_TOKEN = (
    'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjQsImxvZ'
    '2luIjoidGVzdDQiLCJuYW1lIjoidGVzdDQiLCJncm91cCI6IlVzZXIi'
    'fQ.SolZr2F5ITAWSKTJ_kXLk0jHF8MfI8Oua2V7uLX95gE'
)


def test_on_get_books(client, library_service, book_1):
    library_service.take_books_info.return_value = [book_1]

    expected = [
        {
            'authors': 'test_authors_1',
            'desc': 'test_desc_1',
            'id': 1,
            'isbn13': 'test_isbn13_1',
            'language': 'test_language_1',
            'pages': 100,
            'price_USD': 11.1,
            'publisher': 'test_publisher_1',
            'rating': 1.0,
            'subtitle': 'test_subtitle_1',
            'tag': 'test_tag_1',
            'title': 'test_title_1',
            'year': 2001
        }
    ]

    result = client.simulate_get('/api/library/books')

    assert result.status_code == HTTPStatus.OK
    assert result.json == expected


def test_on_get_users_without_authentication(client, library_service, user_1):
    library_service.take_users_info.return_value = [user_1]
    result = client.simulate_get('/api/library/users')
    assert result.status_code == HTTPStatus.BAD_REQUEST


def test_on_get_users(client, library_service, user_1):

    library_service.take_users_info.return_value = [user_1]

    expected = [{'id': 1, 'login': 'test_login_1'}]

    result = client.simulate_get(
        path='/api/library/users',
        headers={'Authorization': f'Bearer {TEST_TOKEN}'}
    )

    assert result.status_code == HTTPStatus.OK
    assert result.json == expected


def test_on_get_books_filter(client, library_service, book_1):
    book_1.price_USD = 41
    params = {'order_by': 'price_USD', 'price_USD': 'gte:40'}

    library_service.take_books_with_filter_and_sort.return_value = [book_1]

    expected = [
        {
            'authors': 'test_authors_1',
            'desc': 'test_desc_1',
            'id': 1,
            'isbn13': 'test_isbn13_1',
            'language': 'test_language_1',
            'pages': 100,
            'price_USD': 41,
            'publisher': 'test_publisher_1',
            'rating': 1.0,
            'subtitle': 'test_subtitle_1',
            'tag': 'test_tag_1',
            'title': 'test_title_1',
            'year': 2001
        },
    ]

    result = client.simulate_get(
        path='/api/library/books_filter',
        headers={'Authorization': f'Bearer {TEST_TOKEN}'},
        params=params
    )

    assert result.status_code == HTTPStatus.OK
    assert result.json == expected


def test_on_get_book(client, library_service, book_1):
    params = {'book_id': 1}
    library_service.take_book_info.return_value = book_1

    expected = {
        'authors': 'test_authors_1',
        'desc': 'test_desc_1',
        'id': 1,
        'isbn13': 'test_isbn13_1',
        'language': 'test_language_1',
        'pages': 100,
        'price_USD': 11.1,
        'publisher': 'test_publisher_1',
        'rating': 1.0,
        'subtitle': 'test_subtitle_1',
        'tag': 'test_tag_1',
        'title': 'test_title_1',
        'year': 2001
    }

    result = client.simulate_get(
        path='/api/library/book',
        headers={'Authorization': f'Bearer {TEST_TOKEN}'},
        params=params
    )

    assert result.status_code == HTTPStatus.OK
    assert result.json == expected


def test_on_get_journal(client, library_service, journal_1):
    journal_1.taking_date = '2022-04-15'
    journal_1.timedelta = '1 day'
    journal_1.returning_date = ''
    library_service.take_self_journal.return_value = [journal_1]

    expected = [
        {
            'book_id': 1,
            'id': 1,
            'returning_date': '',
            'status': 'return',
            'taking_date': '2022-04-15',
            'timedelta': '1 day',
            'user_id': 1
        }
    ]

    result = client.simulate_get(
        path='/api/library/journal',
        headers={'Authorization': f'Bearer {TEST_TOKEN}'},
    )

    assert result.status_code == HTTPStatus.OK
    assert result.json == expected


def test_on_get_active_book(client, library_service, book_1):
    library_service.take_active_book.return_value = book_1
    expected = {
        'authors': 'test_authors_1',
        'desc': 'test_desc_1',
        'id': 1,
        'isbn13': 'test_isbn13_1',
        'language': 'test_language_1',
        'pages': 100,
        'price_USD': 11.1,
        'publisher': 'test_publisher_1',
        'rating': 1.0,
        'subtitle': 'test_subtitle_1',
        'tag': 'test_tag_1',
        'title': 'test_title_1',
        'year': 2001
    }

    result = client.simulate_get(
        path='/api/library/active_book',
        headers={'Authorization': f'Bearer {TEST_TOKEN}'},
    )

    assert result.status_code == HTTPStatus.OK
    assert result.json == expected


def test_on_post_reserve_book(client, library_service, book_1):
    result = client.simulate_post(
        path='/api/library/reserve_book',
        headers={'Authorization': f'Bearer {TEST_TOKEN}'},
        json={'book_id': book_1.id}
    )
    assert result.status_code == HTTPStatus.OK


def test_on_post_return_book(client, library_service):
    result = client.simulate_post(
        path='/api/library/return_book',
        headers={'Authorization': f'Bearer {TEST_TOKEN}'},
        json={}
    )
    assert result.status_code == HTTPStatus.OK


def test_buy_book(client, library_service):
    result = client.simulate_post(
        path='/api/library/buy_book',
        headers={'Authorization': f'Bearer {TEST_TOKEN}'},
        json={}
    )
    assert result.status_code == HTTPStatus.OK
