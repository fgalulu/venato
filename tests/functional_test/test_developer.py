def test_ticket_get_single_authorised(client, authorised_dev, new_ticket):
    """
    GET single ticket with valid token
    """
    response = client.get(f'/developer/tickets/{new_ticket.id}', headers={
        'Authorization': f'Bearer {authorised_dev}'
    })
    assert response.status_code == 200
    assert b'ticket one' in response.data


def test_get_single_ticket_unauthorised(client, authorised_dev, new_ticket):
    """
    Get single ticket with valid token
    """
    response = client.get(f'/developer/tickets/{new_ticket.id}', headers={
                'Authorization': f'Bearer bejfnisomnxc625jsejf'
            })

    assert response.status_code == 401
    assert b'Unauthorized' in response.data


def test_get_none_existing_single_ticket_authorised(client, authorised_dev, new_ticket):
    """
    Get single ticket with valid token
    """
    response = client.get(f'/developer/tickets/4', headers={
                'Authorization': f'Bearer {authorised_dev}'
            })

    assert response.status_code == 404
    assert b'Not Found' in response.data


def test_get_all_ticket_authorised(client, authorised_dev, new_ticket):
    """
    Get all tickets  with valid token.
    """
    response = client.get(f'/developer/tickets/', headers={
        'Authorization': f'Bearer {authorised_dev}'
    })

    assert response.status_code == 200
    # assert b'ticket one' in response.data


def test_get_all_tickets_unauthorised(client):
    """
    Get all tickets with valid token
    """
    response = client.get(f'/developer/tickets/', headers={
                'Authorization': f'Bearer bejfnisomnxc625jsejf'
            })

    assert response.status_code == 401
    assert b'Unauthorized' in response.data


def test_post_tickets_authorised(client, authorised_dev, new_project):
    """
    POST ticket with a valid token.
    """
    payload = {
        "label": "ticket two",
        "desc": "ticket two description",
        "status": "open",
        "project_id": new_project.id
    }
    response = client.post('/developer/tickets/', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_dev}'
    })

    assert response.status_code == 200
    assert b'Ticket with label ticket two created.' in response.data


# def test_get_token_unauthorised(client):
#     """
#         Get token while unauthorised, invalid token
#     """
#     response = client.get('/developer/token', headers={
#                 'Authorization': f'Bearer ejnjcnirgmkmckd54515dfmf'
#             })
#
#     assert response.status_code == 401
#     # assert b'{authorised_admin}' in response.data


def test_get_single_user(client, authorised_dev, new_user):
    """
    Get single user while authorised
    """
    response = client.get(f'/developer/users/{new_user.id}', headers={
                'Authorization': f'Bearer {authorised_dev}'
            })
    assert response.status_code == 200


def test_get_single_user_unauthorised(client, authorised_dev, new_user):
    """
    Get single user while unauthorised, invalid token
    """
    response = client.get(f'/developer/users/{new_user.id}', headers={
                'Authorization': f'Bearer bejfnisomnxc625jsejf'
            })
    assert response.status_code == 401


def test_get_all_user(client, authorised_dev):
    """
    Get all user while authorised
    """
    response = client.get('/developer/users/', headers={
                'Authorization': f'Bearer {authorised_dev}'
            })
    assert response.status_code == 200


def test_get_single_project_authorised(client, authorised_dev, new_project, new_dev_project):
    """
    Get single project with valid token
    """
    response = client.get(f'/developer/projects/{new_project.id}', headers={
                'Authorization': f'Bearer {authorised_dev}'
            })

    assert response.status_code == 200


def test_get_single_project_unauthorised(client, authorised_dev, new_project):
    """
    Get single project with valid token
    """
    response = client.get(f'/developer/projects/{new_project.id}', headers={
                'Authorization': f'Bearer bejfnisomnxc625jsejf'
            })

    assert response.status_code == 401


def test_get_none_existing_single_project_authorised(client, authorised_dev):
    """
    Get single project with valid token
    """
    response = client.get(f'/developer/projects/44', headers={
                'Authorization': f'Bearer {authorised_dev}'
            })

    assert response.status_code == 404


def test_get_all_projects_authorised(client, authorised_dev, new_project):
    """
    Get all projects with valid token
    """
    response = client.get(f'/developer/projects/', headers={
                'Authorization': f'Bearer {authorised_dev}'
            })

    assert response.status_code == 200


def test_get_all_projects_unauthorised(client):
    """
    Get all projects with valid token
    """
    response = client.get(f'/developer/projects/', headers={
                'Authorization': f'Bearer bejfnisomnxc625jsejf'
            })

    assert response.status_code == 401

