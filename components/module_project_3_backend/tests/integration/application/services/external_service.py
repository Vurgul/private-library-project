from http import HTTPStatus

import requests


def test_take_message():
    tag = 'test'
    url_search = 'https://api.itbook.store/1.0/search'
    response = requests.get(f'{url_search}/{tag}')
    assert response.status_code == HTTPStatus.OK
