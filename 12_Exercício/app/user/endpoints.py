from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from user import queries, schemas
from database import SessionLocal, engine, get_db


user_router = APIRouter()


@user_router.get('/user', response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = queries.get_users(db)
    return users


@user_router.post('/user', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = queries.get_user_by_email(db, user_email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return queries.create_user(db=db, user=user)