from typing import List

from pydantic import BaseModel
        
        
class Login(BaseModel):
    email: str
    password: str