from http import HTTPStatus


def test_on_post_registration(client):
    body = {
        "name": "test",
        "login": "test",
        "password": "test"
    }
    result = client.simulate_post('/api/authorization/registration', json=body)
    assert result.status_code == HTTPStatus.OK
    assert result.json is None


def test_on_post_authentication(client):
    params = {
        'login': 'test',
        'password': 'test'
    }

    expected = {
        'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImxvZ2luIj'
        'oidGVzdF9sb2dpbl8xIiwibmFtZSI6InRlc3RfbG9naW5fMSIsImdyb3VwIj'
        'oiVXNlciJ9.a0XryRujR53HXIiOb0cASuQXXK0-TjQvgq4uf8LG_vc'
    }

    result = client.simulate_post(
        '/api/authorization/authentication',
        params=params
    )
    assert result.status_code == HTTPStatus.OK
    assert result.json == expected
