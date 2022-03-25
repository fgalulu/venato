

def test_authenticate(client):
    """
        post to the authetication route without data.
    """
    response = client.post('/authenticate')

    assert response.status_code == 400
    assert b'No email or password provided.' in response.data
    