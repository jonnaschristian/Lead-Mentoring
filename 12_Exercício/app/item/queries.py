from sqlalchemy.orm import Session

from item import models, schemas



def create_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items_by_user_id(db: Session, user_id: int):
    return db.query(models.Item).filter(models.Item.owner_id == user_id).all()