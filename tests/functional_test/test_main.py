from flask import jsonify


# main blueprint
# post request to routes without data
def test_authenticate(client):
    """
        post to the authetication route without data.
    """
    payload = {"email": "",
               "password": ""}
    response = client.post('/authenticate', json=payload, content_type='application/json')

    assert response.status_code == 404
    # assert b'No email or  provided.' in response.data


def test_register(client):
    """
    post to register route with no data
    """
    payload = {
        'email': '',
        'first_name': '',
        'last_name': '',
        'password': ''
    }
    response = client.post('/register', json=payload, content_type='application/json')

    assert response.status_code == 400
    # assert b'' in response.data


# post request to routes with valid data
def test_authenticate_json(client, new_user):
    """
        post to the authetication route with data.
    """
    payload = {'email': new_user.email, 'password': 'Pass1234!'}
    response = client.post('/authenticate', json=payload, content_type='application/json')

    assert response.status_code == 200
    assert b'success' in response.data


def test_register_json(client):
    """
    post to register route with no data
    """
    payload = {
        'email': 't@t.com',
        'first_name': 'first',
        'last_name': 'name',
        'password': 'password'
    }
    response = client.post('/register', json=payload, content_type='application/json')

    assert response.status_code == 200
    assert b'success' in response.data


# post request to routes with invalid data
def test_authenticate_invalid_json(client, new_user):
    """
        post to the authetication route with data.
    """
    payload = {'email': 'some@example.com', 'password': 'Pass1234!'}
    response = client.post('/authenticate', json=payload, content_type='application/json')

    assert response.status_code == 404
    assert b'Not Found' in response.data


def test_register_invalid_json(client):
    """
    post to register route with no data
    """
    payload = {
        'email': '',
        'first_name': 'first',
        'last_name': 'name',
        'password': 'password'
    }
    response = client.post('/register', json=payload, content_type='application/json')

    assert response.status_code == 200
    assert b'success' in response.data


def test_get_token(client, authorised_admin):
    """
        Get token while authorised
    """
    response = client.get('/token', headers={
                'Authorization': f'Bearer {authorised_admin}'
            })

    assert response.status_code == 200
    # assert b'{authorised_admin}' in response.data


def test_get_token_unauthorised(client):
    """
        Get token while unauthorised, invalid token
    """
    response = client.get('/token', headers={
                'Authorization': f'Bearer ejnjcnirgmkmckd54515dfmf'
            })

    assert response.status_code == 401
    # assert b'{authorised_admin}' in response.data

