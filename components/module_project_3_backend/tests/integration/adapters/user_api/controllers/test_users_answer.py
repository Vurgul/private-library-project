def test__on_get_user_info(client, users_service, user_1):
    user_1.id = 1
    user_1.name = 'test'
    user_1.age = 3

    users_service.get_user_info.return_value = user_1

    expected = {
        'name': "test",
        'age': 3,
        'id': 1
    }

    result = client.simulate_get('/api/users/user_info?user_id=1')

    assert result.status_code == 200
    assert result.json == expected
