from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from auth import queries, schemas
from database import SessionLocal, engine, get_db
from utils import hash


app = FastAPI()

auth_router = APIRouter(prefix="/auth")

@auth_router.post('/login')
def login(login: schemas.Login, db: Session = Depends(get_db)):
    user = queries.get_user_by_email(db, login.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user dont exist"
        )
    if hash.verifyhash_password_hashlib(login.password, user.password):
        return JSONResponse({"detail": "success login", "status": status.HTTP_200_OK})
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden"
    )