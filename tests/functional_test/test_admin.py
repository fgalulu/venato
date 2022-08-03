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


def test_put_user_unauthorised(client, new_user):
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



def test_put_none_existing_user_authorised(client, authorised_admin, new_user):
    """
    Put an existing user with invalid token and valid data
    """
    payload = {
        'email': 'test@email.com',
        'first_name': 'test',
        'last_name': 'one',
        'password': ''
    }
    response = client.put(f'/admin/users/4', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404


def test_delete_authorised(client, authorised_admin, new_user):
    """
    Delete an existing user with valid token and valid user
    """
    response = client.delete(f'/admin/users/{new_user.id}', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200


def test_delete_unauthorised(client, new_user):
    """
    Delete an existing user with valid token and valid user
    """
    response = client.delete(f'/admin/users/{new_user.id}', headers={
        'Authorization': f'Bearer bejfnisomnxc625jsejf'
    })

    assert response.status_code == 401


def test_delete_none_existing_user_authorised(client, authorised_admin, new_user):
    """
    Delete an existing user with valid token and valid user
    """
    response = client.delete(f'/admin/users/7', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404


def test_get_single_project_authorised(client, authorised_admin, new_project):
    """
    Get single project with valid token
    """
    response = client.get(f'/admin/projects/{new_project.id}', headers={
                'Authorization': f'Bearer {authorised_admin}'
            })

    assert response.status_code == 200


def test_get_single_project_unauthorised(client, authorised_admin, new_project):
    """
    Get single project with valid token
    """
    response = client.get(f'/admin/projects/{new_project.id}', headers={
                'Authorization': f'Bearer bejfnisomnxc625jsejf'
            })

    assert response.status_code == 401


def test_get_none_existing_single_project_authorised(client, authorised_admin, new_project):
    """
    Get single project with valid token
    """
    response = client.get(f'/admin/projects/4', headers={
                'Authorization': f'Bearer {authorised_admin}'
            })

    assert response.status_code == 404


def test_get_all_projects_authorised(client, authorised_admin, new_project):
    """
    Get all projects with valid token
    """
    response = client.get(f'/admin/projects/', headers={
                'Authorization': f'Bearer {authorised_admin}'
            })

    assert response.status_code == 200


def test_get_all_projects_unauthorised(client):
    """
    Get all projects with valid token
    """
    response = client.get(f'/admin/projects/', headers={
                'Authorization': f'Bearer bejfnisomnxc625jsejf'
            })

    assert response.status_code == 401


def test_post_new_project_authorised(client, authorised_admin, new_pm):
    """
    Post new project with valid token
    """
    payload = {
        'name': 'some project name',
        'desc': 'some description for thw project',
        'supervisor': f'{new_pm.id}'
    }

    response = client.post('/admin/projects/', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200


def test_post_new_project_unauthorised(client, new_pm):
    """
    Post new project with valid token
    """
    payload = {
        'name': 'some project name',
        'desc': 'some description for thw project',
        'supervisor': f'{new_pm.id}'
    }

    response = client.post('/admin/projects/', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer bejfnisomnxc625jsejf'
    })

    assert response.status_code == 401


def test_post_new_project_with_none_pm_as_supervisor(client, authorised_admin, new_admin):
    """
    Post new project with valid token and assign supervisor a none pm user
    """
    payload = {
        'name': 'some project name',
        'desc': 'some description for thw project',
        'supervisor': f'{new_admin.id}'
    }

    response = client.post('/admin/projects/', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404
    assert b'Supervisor doesnt exist.' in response.data


# def test_post
def test_put_project_authorised(client, authorised_admin, new_project, new_pm):
    """
    Put existing project with a valid token and existing project
    """
    payload = {
        'name': 'some project name',
        'desc': 'some description for thw project',
        'supervisor': f'{new_pm.id}'
    }

    response = client.put(f'/admin/projects/{new_project.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200
    assert b'success' in response.data


def test_put_none_existing_project_authorised(client, authorised_admin):
    """
    Put none existing project with a valid token
    """
    payload = {
        'data': ''
    }
    response = client.put(f'/admin/projects/4', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404
    assert b'Not Found' in response.data


def test_put_project_unauthorised(client, new_project, new_pm):
    """
    Put existing project with an invalid  token
    """

    payload = {
        'name': 'some project name',
        'desc': 'some description for thw project',
        'supervisor': f'{new_pm.id}'
    }

    response = client.put(f'/admin/projects/{new_project.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer hiwjdkasuhew5646dnuih'
    })

    assert response.status_code == 401
    assert b'Unauthorized' in response.data


def test_put_project_authorised_with_none_existing_supervisor(client, authorised_admin, new_project):
    """
    Put existing project with an invalid  token
    """

    payload = {
        'name': 'some project name',
        'desc': 'some description for thw project',
        'supervisor': 22
    }

    response = client.put(f'/admin/projects/{new_project.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404
    assert b'Supervisor doesnt exist.' in response.data


def test_project_delete_authorised(client, authorised_admin, new_project):
    """
    Delete project with valid token
    """
    response = client.delete(f'/admin/projects/{new_project.id}', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200
    assert b'Project deleted' in response.data


def test_project_delete_none_existing_authorised(client, authorised_admin):
    """
    Delete none existing project
    """
    response = client.delete(f'/admin/projects/5', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404
    assert b'Not Found' in response.data


# tickets
def test_ticket_get_single_authorised(client, authorised_admin, new_ticket):
    """
    GET single ticket with valid token
    """
    response = client.get(f'/admin/tickets/{new_ticket.id}', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })
    assert response.status_code == 200
    assert b'ticket one' in response.data


def test_get_single_ticket_unauthorised(client, authorised_admin, new_ticket):
    """
    Get single project with valid token
    """
    response = client.get(f'/admin/tickets/{new_ticket.id}', headers={
                'Authorization': f'Bearer bejfnisomnxc625jsejf'
            })

    assert response.status_code == 401
    assert b'Unauthorized' in response.data


def test_get_none_existing_single_ticket_authorised(client, authorised_admin, new_ticket):
    """
    Get single project with valid token
    """
    response = client.get(f'/admin/tickets/4', headers={
                'Authorization': f'Bearer {authorised_admin}'
            })

    assert response.status_code == 404
    assert b'Not Found' in response.data


def test_get_all_ticket_authorised(client, authorised_admin, new_ticket):
    """
    Get all tickets  with valid token.
    """
    response = client.get(f'/admin/tickets/', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200
    assert b'ticket one' in response.data


def test_get_all_tickets_unauthorised(client):
    """
    Get all projects with valid token
    """
    response = client.get(f'/admin/tickets/', headers={
                'Authorization': f'Bearer bejfnisomnxc625jsejf'
            })

    assert response.status_code == 401
    assert b'Unauthorized' in response.data


def test_post_tickets_authorised(client, authorised_admin, new_project):
    """
    POST project with a valid token.
    """
    payload = {
        "label": "ticket two",
        "desc": "ticket two description",
        "status": "open",
        "project_id": new_project.id
    }
    response = client.post('/admin/tickets/', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200
    assert b'Ticket with label ticket two created.' in response.data


def test_put_ticket_authorised(client, authorised_admin, new_ticket, new_project):
    """
    Put existing project with a valid token and existing project
    """
    payload = {
        'label': 'some ticket name',
        'desc': 'some description for the ticket',
        'status': 'in-progress',
        'project_id': new_project.id
    }

    response = client.put(f'/admin/tickets/{new_ticket.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200
    assert b'success' in response.data


def test_put_none_existing_ticket_authorised(client, authorised_admin):
    """
    Put none existing project with a valid token
    """
    payload = {
        'data': ''
    }
    response = client.put(f'/admin/tickets/4', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404
    assert b'Not Found' in response.data


def test_put_tickets_unauthorised(client, new_ticket, new_project):
    """
    Put existing project with an invalid  token
    """

    payload = {
        'label': 'some project name',
        'desc': 'some description for thw project',
        'project_id': new_project.id
    }

    response = client.put(f'/admin/tickets/{new_ticket.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer hiwjdkasuhew5646dnuih'
    })

    assert response.status_code == 401
    assert b'Unauthorized' in response.data


def test_put_tickets_authorised_with_none_existing_project(client, authorised_admin, new_project):
    """
    Put existing project with an invalid  token
    """

    payload = {
        'label': 'some project name',
        'desc': 'some description for the project',
        'status': 'open',
        'project_id': 22
    }

    response = client.put(f'/admin/tickets/{new_project.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404
    assert b'Not Found' in response.data


def test_ticket_delete_authorised(client, authorised_admin, new_ticket):
    """
    Delete project with valid token
    """
    response = client.delete(f'/admin/tickets/{new_ticket.id}', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200
    assert b'deleted' in response.data


def test_tickets_delete_none_existing_authorised(client, authorised_admin):
    """
    Delete none existing project
    """
    response = client.delete(f'/admin/tickets/5', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404
    assert b'Not Found' in response.data


def test_get_user_ticket_authorised(client, authorised_admin, new_user_ticket):
    """
    GET user ticket relationship
    """
    response = client.get(f'/admin/user-tickets/', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200
    assert b'' in response.data


def test_get_user_ticket_unauthorised(client, new_user_ticket):
    """
    GET user ticket relationship unathorised
    """
    response = client.get(f'/admin/user-tickets/', headers={
        'Authorization': 'Bearer ufoshdlfiohf45454'
    })

    assert response.status_code == 401


def test_get_single_user_ticket_authorised(client, authorised_admin, new_user_ticket):
    """
    GET user ticket relationship
    """
    response = client.get(f'/admin/user-tickets/{new_user_ticket.id}', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200
    assert b'' in response.data


def test_get_single_user_ticket_unauthorised(client, new_user_ticket):
    """
    GET user ticket relationship unathorised
    """
    response = client.get(f'/admin/user-tickets/{new_user_ticket.id}', headers={
        'Authorization': 'Bearer ufoshdlfiohf45454'
    })

    assert response.status_code == 401


def test_get_single_none_existing_user_ticket_authorised(client, authorised_admin):
    """
    GET noe existing user ticket relationship with valid token.
    """
    response = client.get(f'/admin/user-tickets/45', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404


def test_post_user_ticket_authorised(client, authorised_admin, new_ticket, new_user):
    """
    POST user ticket relationship
    """
    payload = {
        'user_id': new_user.id,
        'ticket_id': new_ticket.id
    }

    response = client.post(f'/admin/user-tickets/', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200


def test_post_user_ticket_unauthorised(client, authorised_admin, new_ticket, new_user):
    """
    POST user ticket relationship with and invalid token
    """
    payload = {
        'user_id': new_user.id,
        'ticket_id': new_ticket.id
    }

    response = client.post(f'/admin/user-tickets/', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer hifjokeo'
    })

    assert response.status_code == 401


def test_post_nonuser_ticket_authorised(client, authorised_admin, new_ticket):
    """
    POST user ticket relationship with none existing user and a valid token.
    """
    payload = {
        'user_id': 4,
        'ticket_id': new_ticket.id
    }

    response = client.post(f'/admin/user-tickets/', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404


def test_post_user_nonticket_authorised(client, authorised_admin, new_user):
    """
    POST user ticket relationship with none existing ticket and a valid token.
    """
    payload = {
        'user_id': new_user.id,
        'ticket_id': 5
    }

    response = client.post(f'/admin/user-tickets/', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404


def test_put_user_ticket_authorised(client, authorised_admin, new_ticket, new_user, new_user_ticket):
    """
    PUT user ticket relationship
    """
    payload = {
        'user_id': new_user.id,
        'ticket_id': new_ticket.id
    }

    response = client.put(f'/admin/user-tickets/{new_user_ticket.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200


def test_put_user_ticket_unauthorised(client, authorised_admin, new_ticket, new_user, new_user_ticket):
    """
    PUT user ticket relationship with and invalid token
    """
    payload = {
        'user_id': new_user.id,
        'ticket_id': new_ticket.id
    }

    response = client.put(f'/admin/user-tickets/{new_user_ticket.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer hifjokeo'
    })

    assert response.status_code == 401


def test_put_nonuser_ticket_authorised(client, authorised_admin, new_ticket, new_user_ticket):
    """
    PUT user ticket relationship with none existing user and a valid token.
    """
    payload = {
        'user_id': 4,
        'ticket_id': new_ticket.id
    }

    response = client.put(f'/admin/user-tickets/{new_user_ticket.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404


def test_put_user_nonticket_authorised(client, authorised_admin, new_user, new_user_ticket):
    """
    PUT user ticket relationship with none existing ticket and a valid token.
    """
    payload = {
        'user_id': new_user.id,
        'ticket_id': 5
    }

    response = client.put(f'/admin/user-tickets/{new_user_ticket.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404


def test_put_user_ticket_none_existing_authorised(client, authorised_admin, new_user, new_ticket):
    """
    PUT user ticket relationship that doesn't exist
    """
    payload = {
        'user_id': new_user.id,
        'ticket_id': 5
    }

    response = client.put(f'/admin/user-tickets/8', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404


def test_user_ticket_delete_authorised(client, authorised_admin, new_user_ticket):
    """
    Delete project with valid token
    """
    response = client.delete(f'/admin/user-tickets/{new_user_ticket.id}', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200
    assert b'success' in response.data


def test_user_ticket_delete_none_existing_authorised(client, authorised_admin):
    """
    Delete none existing project
    """
    response = client.delete(f'/admin/user-tickets/5', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404
    assert b'Not Found' in response.data


def test_get_user_project_authorised(client, authorised_admin, new_user_project):
    """
    GET user ticket relationship
    """
    response = client.get(f'/admin/user-projects/', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200
    assert b'' in response.data


def test_get_user_project_unauthorised(client, new_user_project):
    """
    GET user ticket relationship unathorised
    """
    response = client.get(f'/admin/user-projects/', headers={
        'Authorization': 'Bearer ufoshdlfiohf45454'
    })

    assert response.status_code == 401


def test_get_single_user_project_authorised(client, authorised_admin, new_user_project):
    """
    GET user project relationship
    """
    response = client.get(f'/admin/user-projects/{new_user_project.id}', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200
    assert b'' in response.data


def test_get_single_user_paroject_unauthorised(client, new_user_project):
    """
    GET user project relationship unauthorised
    """
    response = client.get(f'/admin/user-tickets/{new_user_project.id}', headers={
        'Authorization': 'Bearer ufoshdlfiohf45454'
    })

    assert response.status_code == 401


def test_get_single_none_existing_user_project_authorised(client, authorised_admin):
    """
    GET noe existing user projects relationship with valid token.
    """
    response = client.get(f'/admin/user-projects/45', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404


def test_post_user_project_authorised(client, authorised_admin, new_project, new_user):
    """
    POST user project relationship
    """
    payload = {
        'user_id': new_user.id,
        'project_id': new_project.id
    }

    response = client.post(f'/admin/user-projects/', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200


def test_post_user_projects_unauthorised(client, authorised_admin, new_project, new_user):
    """
    POST user projects relationship with and invalid token
    """
    payload = {
        'user_id': new_user.id,
        'project_id': new_project.id
    }

    response = client.post(f'/admin/user-projects/', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer hifjokeo'
    })

    assert response.status_code == 401


def test_post_nonuser_projects_authorised(client, authorised_admin, new_project):
    """
    POST user projects relationship with none existing user and a valid token.
    """
    payload = {
        'user_id': 4,
        'project_id': new_project.id
    }

    response = client.post(f'/admin/user-projects/', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404


def test_post_user_nonproject_authorised(client, authorised_admin, new_user):
    """
    POST user projects relationship with none existing project and a valid token.
    """
    payload = {
        'user_id': new_user.id,
        'project_id': 5
    }

    response = client.post(f'/admin/user-projects/', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404


def test_put_user_project_authorised(client, authorised_admin, new_ticket, new_user, new_user_project):
    """
    PUT user project relationship
    """
    payload = {
        'user_id': new_user.id,
        'project_id': new_ticket.id
    }

    response = client.put(f'/admin/user-projects/{new_user_project.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200


def test_put_user_project_unauthorised(client, authorised_admin, new_project, new_user, new_user_project):
    """
    PUT user project relationship with and invalid token
    """
    payload = {
        'user_id': new_user.id,
        'ticket_id': new_project.id
    }

    response = client.put(f'/admin/user-tickets/{new_user_project.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer hifjokeo'
    })

    assert response.status_code == 401


def test_put_nonuser_project_authorised(client, authorised_admin, new_ticket, new_user_project):
    """
    PUT user project relationship with none existing user and a valid token.
    """
    payload = {
        'user_id': 4,
        'project_id': new_ticket.id
    }

    response = client.put(f'/admin/user-projects/{new_user_project.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404


def test_put_user_nonproject_authorised(client, authorised_admin, new_user, new_user_project):
    """
    PUT user project relationship with none existing project and a valid token.
    """
    payload = {
        'user_id': new_user.id,
        'project_id': 5
    }

    response = client.put(f'/admin/user-tickets/{new_user_project.id}', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404


def test_put_user_project_none_existing_authorised(client, authorised_admin, new_user, new_project):
    """
    PUT user project relationship that doesn't exist
    """
    payload = {
        'user_id': new_user.id,
        'project_id': 5
    }

    response = client.put(f'/admin/user-projects/8', json=payload, content_type='application/json', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404


def test_user_projects_delete_authorised(client, authorised_admin, new_user_project):
    """
    Delete project with valid token
    """
    response = client.delete(f'/admin/user-projects/{new_user_project.id}', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200
    assert b'success' in response.data


def test_user_project_delete_none_existing_authorised(client, authorised_admin):
    """
    Delete none existing project
    """
    response = client.delete(f'/admin/user-projects/5', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 404
    assert b'Not Found' in response.data


def test_project_assignee(client, authorised_admin, new_project, new_user_project):
    """
    somsom
    """
    response = client.get(f'/admin/projects/{new_project.id}/users', headers={
        'Authorization': f'Bearer {authorised_admin}'
    })

    assert response.status_code == 200
