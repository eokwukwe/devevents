from typing import Any, Dict, List, Type
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.utils import config, hashing
from app.database import models, connection
from app.utils.auth_checker import create_token


SQLALCHEMY_DATABASE_URL = config.settings.test_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def save_data_to_db(session, data: List[Dict[str, Any]],
                    model: Type[models.Base]):
    """
    Save data to the database.

    This function maps the provided data to the specified SQLAlchemy model and adds it to the session.
    It then commits the session to save the data to the database.

    Args:
        session: The SQLAlchemy session to use.
        data: A list of dictionaries where each dictionary represents the data for one instance of the model.
        model: The SQLAlchemy model that the data should be mapped to.

    Returns:
        A list of all instances of the model in the session after the data has been added and the session has been committed.
    """
    data_map = map(lambda event: model(**event), data)

    session.add_all(list(data_map))
    session.commit()
    return session.query(model).all()


def add_event_attendee(session, event: models.Event, attendee: models.User):
    """
    Add a user to the attendees of an event.

    Args:
        session: The SQLAlchemy session to use.
        event: The event to add the attendee to.
        attendee: The user to add to the event's attendees.
    """
    event.attendees.append(attendee)
    session.commit()
    session.refresh(event)


def generate_events(faker, user_id, categories, total=3):
    events_data = []

    for _ in range(total):
        events_data.append({
            "title": faker.sentence(),
            "attendee_total": faker.random_int(1, 100),
            "description": faker.paragraph(),
            "venue": faker.address(),
            "venue_lat": faker.latitude(),
            "venue_lng": faker.longitude(),
            "date": faker.future_datetime(),
            "user_id": user_id,
            "category_id": faker.random_element(categories).id
        })
    return events_data


def generate_users(faker, total=3):
    users_data = []
    hashed_password = hashing.create('password')

    for _ in range(total):
        users_data.append({
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "password": hashed_password
        })
    return users_data


@pytest.fixture()
def session():
    print('Creating test database')
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        print('Closing test database')
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.rollback()
    app.dependency_overrides[connection.get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def auth_client(client, auth_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {auth_token}"
    }

    return client


@pytest.fixture()
def test_users(session, faker):
    users_data = generate_users(faker, 5)
    users = save_data_to_db(session, users_data, models.User)
    return users


@pytest.fixture()
def auth_user(test_users):
    '''
    Return the first user in the list of test users
    '''
    return test_users[0]


@pytest.fixture()
def unauthed_user(test_users):
    '''
    Return the second user in the list of test users
    '''
    return test_users[1]


@pytest.fixture()
def other_users(test_users):
    '''
    Return all users except the first two
    '''
    return test_users[2:]


@pytest.fixture()
def auth_token(auth_user, session):
    return create_token(auth_user.id, session)


@pytest.fixture()
def event_categories(session):
    cat_data = [
        {"name": "Music"},
        {"name": "Food"},
        {"name": "Sports"},
        {"name": "Tech"},
        {"name": "Art"},
    ]

    cat_map = map(lambda category: models.Category(**category), cat_data)

    categories = list(cat_map)
    session.add_all(categories)
    session.commit()
    return session.query(models.Category).all()


@pytest.fixture()
def test_events(session, faker, other_users, event_categories):
    user = faker.random_element(other_users)

    events_data = generate_events(faker, user.id, event_categories)
    events = save_data_to_db(session, events_data, models.Event)

    # add attendees to the events
    for event in events:
        add_event_attendee(session, event, user)

    return events


@pytest.fixture()
def auth_user_events(session, faker, auth_user, event_categories):
    events_data = generate_events(faker, auth_user.id, event_categories)
    events = save_data_to_db(session, events_data, models.Event)

    for event in events:
        add_event_attendee(session, event, auth_user)

    return events


@pytest.fixture()
def unauth_user_events(session, faker, unauthed_user, event_categories):
    events_data = generate_events(faker, unauthed_user.id, event_categories)
    events = save_data_to_db(session, events_data, models.Event)

    for event in events:
        add_event_attendee(session, event, unauthed_user)

    return events
