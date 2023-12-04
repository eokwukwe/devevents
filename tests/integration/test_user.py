from app.database import models
from app.schemas import user_schema


def test_get_users(client, test_users):
    res = client.get("/users")

    assert res.status_code == 200
    assert len(res.json()) == len(test_users)


def test_get_user(auth_client, auth_user):
    res = auth_client.get(f"/users/{auth_user.id}")

    assert res.status_code == 200
    assert res.json()["email"] == auth_user.email

def test_get_user_not_found(auth_client, test_users):
    res = auth_client.get(f"/users/{len(test_users) + 10}")

    assert res.status_code == 404
    assert res.json()["message"] == "The requested resource not found"


def test_create_user(client, faker):
    data = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "password": faker.password()
    }
    res = client.post('/users', json=data)

    assert res.status_code == 201
    assert res.json()['email'] == data["email"]


def test_create_user_validate_required_fields(client):
    res = client.post('/users', json={})

    assert res.status_code == 422
    assert res.json() == {
        "first_name": "Field required",
        "last_name": "Field required",
        "email": "Field required",
        "password": "Field required"
    }


def test_create_user_validate_field_types(client):
    data = {
        "first_name": 2222222,
        "last_name": 2222222,
        "email": "test@com",
        "password": 2222222222
    }
    res = client.post('/users', json=data)

    assert res.status_code == 422
    assert res.json() == {
        "first_name": "Input should be a valid string",
        "last_name": "Input should be a valid string",
        "email": "value is not a valid email address: The part after the @-sign is not valid. It should have a period.",
        "password": "Input should be a valid string"
    }


def test_create_user_validate_password_lenght(client, faker):
    data = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "password": "pass"
    }
    res = client.post('/users', json=data)

    assert res.status_code == 422
    assert res.json() == {
        "password": "String should have at least 8 characters"
    }


def test_create_user_validate_duplicate_email(client, test_users, faker):
    data = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": test_users[0].email,
        "password": faker.password()
    }
    res = client.post('/users', json=data)

    assert res.status_code == 422
    assert res.json() == {
        "email": "This email already exists"
    }


def test_update_user(auth_client, auth_user, faker):
    data = {
        # "first_name": faker.first_name(),
        # "last_name": faker.last_name(),
        "bio": faker.sentence()
    }

    res = auth_client.put(f"/users/{auth_user.id}", json=data)

    assert res.status_code == 200
    assert res.json()["bio"] == data["bio"]
    assert res.json()['email'] == auth_user.email


def test_update_user_validate_duplicate_email(auth_client,
                                              auth_user, test_users):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I am a software engineer",
        "email": test_users[2].email
    }

    res = auth_client.put(f"/users/{auth_user.id}", json=data)

    assert res.status_code == 422
    assert res.json()['email'] == 'This email already exists'


def test_change_password(auth_client, auth_user):
    res = auth_client.put(f"/users/{auth_user.id}/password", json={
        "password": "password",
        "new_password": "new_password"
    })

    assert res.status_code == 200
    assert res.json()['message'] == 'Password update successful'


def test_change_password_validate_correct_old_password(auth_client,
                                                       auth_user):
    res = auth_client.put(f"/users/{auth_user.id}/password", json={
        "password": "wrongpassword",
        "new_password": "new_password"
    })

    assert res.status_code == 422
    assert res.json()['password'] == 'Incorrect old password'


def test_delete_user(auth_client, auth_user, session, test_users):
    res = auth_client.delete(f"/users/{auth_user.id}")

    remaining_users = session.query(models.User).all()

    assert res.status_code == 204
    assert len(remaining_users) == len(test_users) - 1
