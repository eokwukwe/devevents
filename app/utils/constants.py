RESPONSE_TEMPLATES = {
    401: {
        "description": "Missing, invalid or expired token",
        "content": {
            "application/json": {
                "example": {
                    "message": "Unauthorized: Missing or invalid authentication token"
                }
            }
        }
    },
    403: {
        "description": "Invalid login credentials",
        "content": {
            "application/json": {
                "example": {"message": "Invalid credentials"}
            }
        }
    },
    404: {
        "description": "The requested resource was not found",
        "content": {
            "application/json": {
                "example": {"message": "Request resource not found"}
            }
        }
    },
    422: {
        "description": "Validation error",
        "content": {
            "application/json": {
                "example": {"first_name": "Field required"}
            }
        }
    },
}

ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg"}
