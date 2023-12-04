from fastapi import APIRouter, BackgroundTasks, Request

from app.utils import email

router = APIRouter(
    tags=["home"],
)


@router.get("/", response_model=None)
async def root(background_tasks: BackgroundTasks, request: Request):
    message = email.MessageSchema(
        subject="Fastapi-Mail module",
        recipients=["denja@mail.com"],
        template_body={"host_name": 'Maddy', "attendee_name": 'Denja man',
                       'attendee_email': 'bork.makdkd@mail.com'},
        subtype=email.MessageType.html
    )

    background_tasks.add_task(
        email.email_client.send_message, message, template_name="attendee.html")
    # await email.email_client.send_message(message, template_name="attendee.html")
    return {"message": "Hello World", "base_url": request.base_url._url}
