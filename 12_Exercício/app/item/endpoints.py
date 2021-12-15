from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic.types import OptionalInt
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from item import queries, models, schemas
from database import SessionLocal, engine, get_db

from utils import hash

models.Base.metadata.create_all(bind=engine)

item_router = APIRouter()


@item_router.get('/items/user/{user_id}')
def get_items(user_id: int, db: Session = Depends(get_db)):
    user = queries.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user dont exist"
        )
    return queries.get_items_by_user_id(db, user_id)

@item_router.post('/user/{user_id}', response_model=schemas.Item)
def create_item(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    user = queries.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user dont exist"
        )
    return queries.create_item(db, item, user_id)