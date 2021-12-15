from sqlalchemy.orm import Session

import hashlib

import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    # db_user = models.User(**user.dict())
    user_dict = user.dict()
    db_user = models.User(
        name=user_dict["name"],
        email=user_dict["email"],
        password= hashlib.md5(user_dict["password"].encode('utf-8')).hexdigest()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


def get_users(db: Session):
    return db.query(models.User).all()
    

def get_items_by_user_id(db: Session, user_id: int):
    return db.query(models.Item).filter(models.Item.owner_id == user_id).all()