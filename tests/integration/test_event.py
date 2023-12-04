from pprint import pprint
from tests.conftest import add_event_attendee


def test_get_event_categories(client, event_categories):
    res = client.get("/events/categories")

    assert res.status_code == 200
    assert len(res.json()) == len(event_categories)


def test_get_events(auth_client, test_events):
    res = auth_client.get("/events")

    assert res.status_code == 200
    assert len(res.json()) == len(test_events)


def test_create_event(auth_client, faker, auth_user, event_categories):
    event_data = {
        "title": faker.sentence(),
        "description": faker.paragraph(),
        "attendee_total": faker.random_int(1, 100),
        "venue": faker.address(),
        "venue_lat": float(faker.latitude()),
        "venue_lng": float(faker.longitude()),
        "date": str(faker.date_time()),
        "user_id": auth_user.id,
        "category_id": faker.random_element(event_categories).id
    }

    res = auth_client.post("/events", json=event_data)

    assert res.status_code == 201
    assert res.json()["title"] == event_data["title"]
    assert res.json()["description"] == event_data["description"]
    assert res.json()["venue"] == event_data["venue"]


def test_create_event_validate_required_field(auth_client):
    res = auth_client.post("/events", json={})

    assert res.status_code == 422
    assert res.json() == {
        "title": "Field required",
        "description": "Field required",
        "attendee_total": "Field required",
        "venue": "Field required",
        "venue_lat": "Field required",
        "venue_lng": "Field required",
        "date": "Field required",
        "category_id": "Field required"
    }


def test_create_event_validate_category_exists(auth_client, faker, auth_user, event_categories):
    event_data = {
        "title": faker.sentence(),
        "description": faker.paragraph(),
        "attendee_total": faker.random_int(1, 100),
        "venue": faker.address(),
        "venue_lat": float(faker.latitude()),
        "venue_lng": float(faker.longitude()),
        "date": str(faker.date_time()),
        "user_id": auth_user.id,
        "category_id": len(event_categories) + 1
    }

    res = auth_client.post("/events", json=event_data)

    assert res.status_code == 422
    assert res.json() == {
        "category_id": "The category does not exist"
    }


def test_get_event(auth_client, test_events):
    event = test_events[0]
    res = auth_client.get(f"/events/{event.id}")

    assert res.status_code == 200
    assert res.json()["title"] == event.title
    assert res.json()["description"] == event.description
    assert res.json()["venue"] == event.venue
    assert res.json()['user']['id'] == event.user_id


def test_get_event_not_found(auth_client, test_events):
    id = len(test_events) + 1
    res = auth_client.get(f"/events/{id}")

    assert res.status_code == 404
    assert res.json() == {
        "message": "The requested resource not found"
    }


def test_get_event_unauthorized(client, test_events):
    event = test_events[0]
    res = client.get(f"/events/{event.id}")

    assert res.status_code == 401
    assert res.json() == {
        "message": "Authorization header not provided"
    }


def test_get_auth_user_events(auth_client, auth_user_events):
    res = auth_client.get("/users/events")

    assert res.status_code == 200
    assert len(res.json()) == len(auth_user_events)


def test_get_any_user_events(auth_client, unauthed_user, unauth_user_events):
    res = auth_client.get(f"/users/{unauthed_user.id}/events")

    assert res.status_code == 200
    assert len(res.json()['events']) == len(unauth_user_events)


def test_update_event(auth_client, auth_user_events):
    update_data = {
        'title': 'Updated title',
        'description': 'Updated description',
    }

    res = auth_client.put(
        f"/events/{auth_user_events[0].id}", json=update_data)

    assert res.status_code == 200
    assert res.json()['title'] == update_data['title']


def test_upate_event_only_owner_can_update(auth_client, unauth_user_events):
    update_data = {
        'title': 'Updated title',
        'description': 'Updated description',
    }

    res = auth_client.put(
        f"/events/{unauth_user_events[0].id}", json=update_data)

    assert res.status_code == 403
    assert res.json() == {
        "message": "You can only update your own events"
    }


def test_delete_event(auth_client, auth_user_events):
    res = auth_client.delete(
        f"/events/{auth_user_events[0].id}")

    assert res.status_code == 204


def test_event_attendee(auth_client, auth_user, unauth_user_events):
    res = auth_client.put(
        f"/events/{unauth_user_events[0].id}/attendees")

    assert res.status_code == 200
    assert auth_user.id in list(
        map(lambda user: user['id'], res.json()['attendees']))


def test_event_attendee_already_attending(session,
                                          auth_client, auth_user, unauth_user_events):
    event = unauth_user_events[0]
    add_event_attendee(session, event, auth_user)

    res = auth_client.put(f"/events/{event.id}/attendees")

    assert res.status_code == 403
    assert res.json() == {
        'message': 'You are already an attendee to this event'
    }


def test_event_attendee_prevent_over_attendance(session, other_users,
                                                auth_client,
                                                unauth_user_events):
    event = unauth_user_events[0]
    event.attendee_total = 2
    event.attendees.append(other_users[0])
    event.attendees.append(other_users[1])

    session.add(event)
    session.commit()
    session.refresh(event)

    res = auth_client.put(f"/events/{event.id}/attendees")

    assert res.status_code == 403
    assert res.json() == {
        'message': 'Event is already full'
    }


def test_event_attendee_host_cannot_apply_as_an_attendee(auth_client, auth_user_events):
    event = auth_user_events[0]

    res = auth_client.put(f"/events/{event.id}/attendees")

    assert res.status_code == 403
    assert res.json() == {
        'message': 'You are the event host. So you are already an attendee'
    }
