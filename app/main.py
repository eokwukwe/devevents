import os
import cloudinary
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.utils import load_routers, config
from app.utils import custom_responses, constants
from app.middlewares.rate_limiter import RateLimitMiddleware
from app.utils.rate_limiter import RateLimiter


# models.Base.metadata.create_all(bind=connection.engine)

app = FastAPI(
    title='Devevents API',
    description='Event management system API for developers',
    responses=constants.RESPONSE_TEMPLATES,
)

cloudinary.config(
    cloud_name=config.settings.cloudinary_name,
    api_key=config.settings.cloudinary_api_key,
    api_secret=config.settings.cloudinary_api_secret
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return custom_responses.validation_error_response(exc)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return custom_responses.http_exception_response(exc)

# @app.exception_handler(SQLAlchemyError)
# async def handle_sqlalchemy_error(request: Request, exc: SQLAlchemyError):
#     # print('>>>>>>>>>>>>>>', exc)
#     # print(type(exc))
#     # if isinstance(exc, IntegrityError):
#     #     if isinstance(exc.orig, UniqueViolation):
#     #         return JSONResponse(
#     #             status_code=400,
#     #             content={"message": "A unique constraint was violated."},
#     #         )
#     #     return JSONResponse(
#     #         status_code=400,
#     #         content={"message": "A database integrity error occurred."},
#     #     )
#     return JSONResponse(
#         status_code=400,
#         content={"message": str(exc)}
#     )

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    RateLimitMiddleware,
    rate_limiter=RateLimiter(),
)

# Load the routers
current_dir_path = os.path.dirname(os.path.abspath(__file__))
router_dir = os.path.join(current_dir_path, 'routers')

load_routers.load_routers(app=app, router_dir=router_dir)
