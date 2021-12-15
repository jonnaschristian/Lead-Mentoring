from typing import List, Dict
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
from pathlib import Path
from fastapi.responses import FileResponse


app = FastAPI()

users: List[dict] = []

class UserSchema(BaseModel):
    name: str
    age: int


class UserUpdateSchema(BaseModel):
    name: str = None
    age: int = None


@app.get('/user') # Solicitação de dados
def get_user():
    return users


@app.post('/user') # Envio de dados
def post_user(user: UserSchema):
    _user = user.dict()
    _user["id"] = uuid.uuid4().hex
    users.append(_user)
    return JSONResponse({"msg": "user created"}, status_code=200)


@app.put('/user/{id}') # Atualizar
def put_user(user: UserSchema, id: str):
    for i in range(len(users)):
        if users[i]["id"] == id:
            _user = user.dict()
            _user["id"] = users[i]["id"]
            users[i] = _user
            return JSONResponse({"msg": "user updated"}, status_code=200)
    return JSONResponse({"msg": "not found"}, status_code=404)


@app.delete('/user/{id}') # Deleta
def delete_user(id: str):
    for i in range(len(users)):
        if users[i]["id"] == id:
            del users[i]
            return JSONResponse({"msg": "user removed"}, status_code=200)
    return JSONResponse({"msg": "not found"}, status_code=404)


@app.patch('/user/{id}') # Atualizar parcialmente
def patch_user(user: UserUpdateSchema, id: str):
    for i in range(len(users)):
        if users[i]["id"] == id:
            users[i].update(user.dict(exclude_unset=True))
            return JSONResponse({"msg": "user updated"}, status_code=200)
    return JSONResponse({"msg": "not found"}, status_code=404)


@app.get("/file")
def get_file():
    return FileResponse("requirements.txt")
