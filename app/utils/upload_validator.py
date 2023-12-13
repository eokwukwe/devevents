import magic
from typing import Set
from fastapi import UploadFile, HTTPException, status


def mega_bytes_to_bytes(mega_bytes: int):
    return mega_bytes * 1024 * 1024


def validate_file(file: UploadFile, max_size: int,  allowed_types: Set[str]):
    """
    Validate the size and type of an uploaded file.

    Args:
        file (UploadFile): The file uploaded by the user.
        max_size (int): Maximum allowed file size in megabytes.
        allowed_types (set): Set of allowed MIME types.

    Raises:
        HTTPException: If the file is too large, the file type is not supported, or an error occurs during validation.
    """

    # Convert max size to bytes
    max_size_bytes = mega_bytes_to_bytes(max_size)

    # Check file size
    file_size = file.file.seek(0, 2)
    file.file.seek(0)

    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File is too large. Max file size is {max_size}MB")

    # Check file type using magic numbers
    file_bytes = file.file.read(1024)  # Read the first 1024 bytes
    file.file.seek(0)
    file_type = magic.from_buffer(file_bytes, mime=True)

    if file_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type. Allowed types are: " + ", ".join(allowed_types))
