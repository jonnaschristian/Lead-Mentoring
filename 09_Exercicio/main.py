from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
import hashlib

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():     
    db = SessionLocal()
    try:         
        yield db     
    finally:
        db.close()


# @app.get('/user')
# def get_user():
#    return models.User.name


#@app.get("/users", response_model=List[schemas.User])
#def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#    users = crud.get_users(db, skip=skip, limit=limit)
#    return users

@app.get("/user", response_model=List[schemas.User])
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
    hash = hashlib.md5(user.password.encode('utf-8')).hexdigest()
    user.password = hash
    return crud.create_user(db=db, user=user)