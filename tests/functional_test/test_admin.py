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


# def test_post