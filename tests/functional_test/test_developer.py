def test_ticket_get_single_authorised(client, authorised_submitter, new_ticket):
    """
    GET single ticket with valid token
    """
    response = client.get(f'/submitter/tickets/{new_ticket.id}', headers={
        'Authorization': f'Bearer {authorised_submitter}'
    })
    assert response.status_code == 200
    assert b'ticket one' in response.data


def test_get_single_ticket_unauthorised(client, authorised_admin, new_ticket):
    """
    Get single ticket with valid token
    """
    response = client.get(f'/submitter/tickets/{new_ticket.id}', headers={
                'Authorization': f'Bearer bejfnisomnxc625jsejf'
            })

    assert response.status_code == 401
    assert b'Unauthorized' in response.data


def test_get_none_existing_single_ticket_authorised(client, authorised_submitter, new_ticket):
    """
    Get single ticket with valid token
    """
    response = client.get(f'/submitter/tickets/4', headers={
                'Authorization': f'Bearer {authorised_submitter}'
            })

    assert response.status_code == 404
    assert b'Not Found' in response.data


def test_get_all_ticket_authorised(client, authorised_submitter, new_ticket):
    """
    Get all tickets  with valid token.
    """
    response = client.get(f'/submitter/tickets/', headers={
        'Authorization': f'Bearer {authorised_submitter}'
    })

    assert response.status_code == 200
    assert b'ticket one' in response.data


def test_get_all_tickets_unauthorised(client):
    """
    Get all tickets with valid token
    """
    response = client.get(f'/submitter/tickets/', headers={
                'Authorization': f'Bearer bejfnisomnxc625jsejf'
            })

    assert response.status_code == 401
    assert b'Unauthorized' in response.data


def test_post_tickets_authorised(client, authorised_submitter, new_project):
    """
    POST ticket with a valid token.
    """
    payload = {
        "label": "ticket two",
        "desc": "ticket two description",
        "status": "open",
        "project_id": new_project.id
    }
    response = client.post('/submitter/tickets/', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_submitter}'
    })

    assert response.status_code == 200
    assert b'Ticket with label ticket two created.' in response.data
