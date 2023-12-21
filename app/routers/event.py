import datetime
import cloudinary.uploader
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from app.database import models
from app.schemas import event_schema
from app.utils import upload_validator, constants
from app.utils import http_helper, logger, geocoding
from app.utils.auth_checker import get_current_user, get_db

router = APIRouter(
    prefix="/events",
    tags=["events"]
)

# Dependency to fetch an event resource
fetch_event = http_helper.get_resource(models.Event)


@router.get("/categories", response_model=list[event_schema.Category])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories


@router.get("", response_model=list[event_schema.Event])
def get_events(db: Session = Depends(get_db), _=Depends(get_current_user)):
    events = db.query(models.Event).all()
    return events


@router.post("", response_model=event_schema.EventOnly,
             status_code=status.HTTP_201_CREATED)
def create_event(payload: event_schema.CreateEvent,
                 db: Session = Depends(get_db),
                 user: models.User = Depends(get_current_user)):

    # Validate the category exists
    category_exists = db.query(models.Category).filter(
        models.Category.id == payload.category_id).first()

    if not category_exists:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'category_id': "The category does not exist"})

    try:

        latlng = geocoding.get_latlng(payload.venue)
        event = models.Event(**payload.model_dump())

        event.user_id = user.id
        event.venue_lat = latlng['lat']
        event.venue_lng = latlng['lng']

        # Add the event owner as an attendee
        event.attendees.append(user)

        db.add(event)
        db.commit()
        db.refresh(event)

    except Exception as e:
        logger.http_logger.error(repr(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return event


@router.get("/{id}", response_model=event_schema.Event)
def get_event(event: models.Event = Depends(fetch_event),
              _=Depends(get_current_user)):
    return event


@router.put("/{id}", response_model=event_schema.EventOnly)
def update_event(payload: event_schema.UpdateEvent,
                 db: Session = Depends(get_db),
                 event: models.Event = Depends(fetch_event),
                 user: models.User = Depends(get_current_user)):
    if event.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can only update your own events")

    try:
        event.date = payload.date or event.date
        event.title = payload.title or event.title
        event.description = payload.description or event.description
        event.category_id = payload.category_id or event.category_id
        event.attendee_total = payload.attendee_total or event.attendee_total
        event.updated_at = datetime.datetime.utcnow()

        if payload.venue:
            latlng = geocoding.get_latlng(payload.venue)
            event.venue_lat = latlng['lat']
            event.venue_lng = latlng['lng']
            event.venue = payload.venue

        db.commit()
        db.refresh(event)

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'category_id': "The category does not exist"})

    except Exception as e:
        logger.http_logger.error(repr(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return event


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event: models.Event = Depends(fetch_event),
                 db: Session = Depends(get_db),
                 user: models.User = Depends(get_current_user)):
    if event.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can only delete your own events")

    db.delete(event)
    db.commit()
    return None


# https://github.com/tiangolo/fastapi/discussions/9067#discussioncomment-5221288
@router.put("/{id}/cover-image", status_code=200, generate_unique_id_function=lambda _: "EventCoverImage", response_model=event_schema.EventOnly)
def event_cover_image(cover_image: UploadFile,
                      db: Session = Depends(get_db),
                      event: models.Event = Depends(fetch_event),
                      user: models.User = Depends(get_current_user)):
    if event.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can only update your own events")

    try:
        # Validate file type and size
        upload_validator.validate_file(
            max_size=2,
            file=cover_image,
            allowed_types=constants.ALLOWED_IMAGE_TYPES)

        # Upload image to cloudinary
        contents = cover_image.file.read()
        response = cloudinary.uploader.upload(contents, folder='devevents')

        event.cover_image = response['secure_url']
        event.updated_at = datetime.datetime.utcnow()

        db.commit()
        db.refresh(event)

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.http_logger.error(f'Covers image upload error: {repr(e)}')

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Could not upload image. Try again.')

    finally:
        cover_image.file.close()

    return event


@router.put('/{id}/attendees', response_model=event_schema.EventOnly)
def attend_event(user: models.User = Depends(get_current_user),
                 event: models.Event = Depends(fetch_event),
                 db: Session = Depends(get_db)):
    if event.user_id == user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are the event host. So you are already an attendee")

    '''
    Because the host is attended to the attendees list by default, the total
    number of attendees will always be one more than the specific number.
    So we need to subtract one from the total number of attendees    
    '''
    if event.attendee_total == len(event.attendees) - 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Event is already full")

    if user in event.attendees:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are already an attendee to this event")

    event.attendees.append(user)
    db.commit()
    db.refresh(event)

    return event


@router.delete('/{id}/attendees', status_code=status.HTTP_204_NO_CONTENT)
def unattend_event(user: models.User = Depends(get_current_user),
                   event: models.Event = Depends(fetch_event),
                   db: Session = Depends(get_db)):
    if event.user_id == user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are the event host. So you cannot unattend")

    if user not in event.attendees:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not an attendee to this event")

    event.attendees.remove(user)
    db.commit()

    return
