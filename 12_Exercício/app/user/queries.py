from sqlalchemy.orm import Session
from user import models, schemas
from utils import hash

def create_user(db: Session, user: schemas.UserCreate):
    # db_user = models.User(**user.dict())
    user_dict = user.dict()
    db_user = models.User(
        name=user_dict["name"],
        email=user_dict["email"],
        password = hash.hash_password_hashlib("password")
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


def get_users(db: Session):
    return db.query(models.User).all()