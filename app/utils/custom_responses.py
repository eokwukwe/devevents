from typing import Dict
from fastapi import HTTPException
from pydantic import ValidationError
from fastapi.responses import JSONResponse


def validation_error_response(error: ValidationError) -> Dict[str, str]:
    """
    Custom validation error response for pydantic ValidationError.

    Example:
    {
        "title": "Title is required",
        "content": "Content is required"
    }

    :param error: ValidationError object
    :return: Dict[str, str]
    """
    response = {}

    for e in error.errors():
        response[e['loc'][1]] = e['msg']

    return JSONResponse(
        status_code=422,
        content=response
    )


def http_exception_response(exce: HTTPException):
    messages = {
        401: "Unauthorized: Missing or invalid authentication token.",
        404: "The requested resource not found",
        405: "Method not allowed",
        500: "Something went wrong. Please contact the administrator",
    }

    if (exce.status_code == 422):
        content = exce.detail
    elif (exce.status_code == 401 or exce.status_code == 403):
        content = {"message": exce.detail or messages[exce.status_code]}
    else:
        content = {"message": messages[exce.status_code] or exce.detail}

    return JSONResponse(
        status_code=exce.status_code,
        content=content,
    )
