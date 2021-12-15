from typing import List
from item import schemas
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    items: List[schemas.Item] = []                  
    class Config:         
        orm_mode = True