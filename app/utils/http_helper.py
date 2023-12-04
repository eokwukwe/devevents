from typing import Type, Callable
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request, status

from app.database.connection import get_db


def get_resource(model: Type) -> Callable:
    def _get_resource(id: int, db: Session = Depends(get_db)):
        resource = db.query(model).filter(model.id == id).first()

        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

        return resource
    return _get_resource


def check_duplicate(model: Type, field: str) -> Callable:
    async def _check_duplicate(request: Request, db: Session = Depends(get_db)):
        payload = await request.json()
        value = payload.get(field)

        if value:
            exists = db.query(model).filter(
                getattr(model, field) == value).first()

            if exists:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={
                        field: f"This {field} already exists"}
                )
    return _check_duplicate
