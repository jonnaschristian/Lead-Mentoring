from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic.types import OptionalInt
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
import crud, models, schemas
from database import SessionLocal, engine
import hashlib

from utils import verifyhash_password_hashlib

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

auth_router = APIRouter(prefix="/auth")


def get_db():     
    db = SessionLocal()
    try:         
        yield db     
    finally:
        db.close()
        

@app.get('/user', response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users

@app.post('/user', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)

@app.post('/user/{user_id}', response_model=schemas.Item)
def create_item(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user dont exist"
        )
    return crud.create_item(db, item, user_id)

@app.get('/items/user/{user_id}')
def get_items(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user dont exist"
        )
    return crud.get_items_by_user_id(db, user_id)



@auth_router.post('/login')
def login(login: schemas.Login, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, login.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user dont exist"
        )
    if verifyhash_password_hashlib(login.password, user.password):
        return JSONResponse({"detail": "success login", "status": status.HTTP_200_OK})
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden"
    )

app.include_router(auth_router)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", reload=True)
