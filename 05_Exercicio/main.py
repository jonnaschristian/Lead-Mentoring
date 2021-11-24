from typing import List
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()

users: List[dict] = []

class UserSchema(BaseModel):
    name: str
    age: int


class UserUpdateSchema(BaseModel):
    name: str = None
    age: int = None


@app.get('/user') # Ver
def get_user():
    return users


@app.post('/user') # Criar
def post_user(user: UserSchema):
    # return {**user, "status": "success"}
    users.append(user.dict())
    return {
        "msg": "user created"
    }


@app.put('/user/{name}') # Atualizar
def put_user(user: UserSchema, name: str):
    for i in range(len(users)):
        if users[i]["name"] == name:
            users[i] = user.dict()
            return JSONResponse({"msg": "user updated"}, status_code=200)
    return JSONResponse({"msg": "not found"}, status_code=404)


@app.delete('/user/{name}')
def delete_user(name: str):
    for i in range(len(users)):
        if users[i]["name"] == name:
            del users[i]
            return JSONResponse({"msg": "user removed"}, status_code=200)
    return JSONResponse({"msg": "not found"}, status_code=404)


@app.patch('/user/{name}') # Atualizar parcialmente
def patch_user(user: UserUpdateSchema, name: str):
    for i in range(len(users)):
        if users[i]["name"] == name:
            users[i].update(user.dict(exclude_unset=True))
            return JSONResponse({"msg": "user updated"}, status_code=200)
    return JSONResponse({"msg": "not found"}, status_code=404)