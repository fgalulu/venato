def test_get_token(client, authorised_admin):
    """
        Get token while authorised
    """
    response = client.get('/admin/token', headers={
                'Authorization': f'Bearer {authorised_admin}'
            })

    assert response.status_code == 200
    # assert b'{authorised_admin}' in response.data


def test_get_token_unauthorised(client):
    """
        Get token while unauthorised, invalid token
    """
    response = client.get('/admin/token', headers={
                'Authorization': f'Bearer ejnjcnirgmkmckd54515dfmf'
            })

    assert response.status_code == 401
    # assert b'{authorised_admin}' in response.data


def test_get_single_user(client, authorised_admin, new_user):
    """
    Get single user while authorised
    """
    response = client.get(f'/admin/users/{new_user.id}', headers={
                'Authorization': f'Bearer {authorised_admin}'
            })
    assert response.status_code == 200


def test_get_single_user_unauthorised(client, authorised_admin, new_user):
    """
    Get single user while unauthorised, invalid token
    """
    response = client.get(f'/admin/users/{new_user.id}', headers={
                'Authorization': f'Bearer bejfnisomnxc625jsejf'
            })
    assert response.status_code == 401


def test_get_all_user(client, authorised_admin):
    """
    Get all user while authorised
    """
    response = client.get('/admin/users/', headers={
                'Authorization': f'Bearer {authorised_admin}'
            })
    assert response.status_code == 200


def test_get_all_user_unauthorised(client):
    """
    Get all user with invalid token
    """
    response = client.get(f'/admin/users/', headers={
                'Authorization': f'Bearer bejfnisomnxc625jsejf'
            })
    assert response.status_code == 401


def test_post_user_authorised(client, authorised_admin):
    """
    Post new user with valid token and data
    """
    payload = {
        'email': 'test@email.com',
        'first_name': 'test',
        'last_name': 'one',
    }
    response = client.post('/admin/users/', json=payload, content_type='application/json',  headers={
                'Authorization': f'Bearer {authorised_admin}'
            })

    assert response.status_code == 201


def test_post_user_unauthorised(client, authorised_admin):
    """
    Post new user with invalid token and valid data
    """
    payload = {
        'email': 'test@email.com',
        'first_name': 'test',
        'last_name': 'one',
    }
    response = client.post('/admin/users/', json=payload, content_type='application/json',  headers={
                'Authorization': 'Bearer bejfnisomnxc625jsejf'
            })

    assert response.status_code == 401


def test_put_user_authorised(client, authorised_admin, new_user):
    """
    Put an existing user with valid token and data
    """
    payload = {
        'email': 'test@email.com',
        'first_name': 'test',
        'last_name': 'one',
        'password': ''
    }
    response = client.put(f'/admin/users/{new_user.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200


def test_put_user_unauthorised(client, authorised_admin, new_user):
    """
    Put an existing user with invalid token and valid data
    """
    payload = {
        'email': 'test@email.com',
        'first_name': 'test',
        'last_name': 'one',
        'password': ''
    }
    response = client.put(f'/admin/users/{new_user.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer bejfnisomnxc625jsejf'
    })

    assert response.status_code == 401
