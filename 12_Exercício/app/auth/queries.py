from sqlalchemy.orm import Session

from auth import schemas

from user import models
from utils import hash

from utils import hash
def autentication(db: Session, login: schemas.Login):
    login_dict = login.dict()
    db_login = models.User(
        email=login_dict["email"],
        password= hash.hash_password_hashlib("password")
    )
    return db_login