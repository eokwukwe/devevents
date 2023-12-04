from app.database import models


def test_login_validate_required_fields(client):
    res = client.post('/auth/login', json={})

    assert res.status_code == 422
    assert res.json() == {
        "email": "Field required",
        "password": "Field required"
    }


def test_login_validate_field_types(client):
    data = {
        "email": 2222222,
        "password": 2222222222
    }
    res = client.post('/auth/login', json=data)

    assert res.status_code == 422
    assert res.json() == {
        "email": "Input should be a valid string",
        "password": "Input should be a valid string"
    }


def test_login_invalid_credentials_wrong_email(client):
    res = client.post('/auth/login', json={
        'email': 'whatiswrongofthewrongemail@email.com',
        'password': 'password'
    })

    assert res.status_code == 401
    assert res.json() == {
        "message": "Invalid credentials"
    }


def test_login_invalid_credentials_wrong_password(client, unauthed_user):
    res = client.post('/auth/login', json={
        'email': unauthed_user.email,
        'password': 'wrongpassword'
    })

    assert res.status_code == 401
    assert res.json() == {
        "message": "Invalid credentials"
    }


def test_login_vaild_credentials(client, unauthed_user, session):
    res = client.post('/auth/login', json={
        'email': unauthed_user.email,
        'password': 'password'
    })

    access_token = session.query(models.AccessToken).filter(
        models.AccessToken.user_id == unauthed_user.id).first()

    assert res.status_code == 200
    assert res.json()['token_type'] == 'bearer'
    assert res.json()['access_token'] == access_token.token


def test_logout_no_auth_token(client):
    res = client.delete('/auth/logout')

    assert res.status_code == 401
    assert res.json() == {
        "message": "Authorization header not provided"
    }


def test_logout_invalid_auth_token(client):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer invalidtokendsslaldfjsdfjld"
    }
    res = client.delete('/auth/logout')

    assert res.status_code == 401
    assert res.json() == {
        "message": "Invalid or expired token"
    }


def test_logout_invalid_incomplete_token(client):
    client.headers = {
        **client.headers,
        "Authorization": f"invalidtokendsslaldfjsdfjld"
    }
    res = client.delete('/auth/logout')

    assert res.status_code == 401
    assert res.json() == {
        "message": "Invalid authorization header. Must start with Bearer"
    }


def test_logout_valid_auth_token(auth_client):
    res = auth_client.delete('/auth/logout')

    assert res.status_code == 204
