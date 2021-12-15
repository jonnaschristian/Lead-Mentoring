import pathlib
from typing import List, Dict
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
from pathlib import Path
from fastapi.responses import FileResponse
from prettytable import PrettyTable

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
    # arquivo = open('relatorio.txt', 'w')
    # lista = [(info['name'], info['age']) for info in users]
    # aux = str(lista)
    # for caractere in "[(',)]":
    #     aux = aux.replace(caractere, '')
    # info = aux.split()
    # print(info)
    # idade = [int(idade) for idade in info if idade.isdigit()]
    # #nome = [str(nome) for nome in info if no]
    # print(idade)
    # arquivo.write('Usuários:\n\nNome            Idade\n')
    # aux2 = str(idade)
    # for caractere in "[]":
    #     aux2 = aux2.replace(caractere, '')
    # for i in range(1):
    #     arquivo.write(f'{info[i]} {aux2:<10}')
    # arquivo.close()
    # file = Path.home()
    # return FileResponse("relatorio.txt", media_type='application/octet-stream')

    x = PrettyTable()

    x.field_names = ["Name", "Age"]
    for user in users:
        x.add_row([user.get("name", ""), user.get("age", "")])

    with open("relatorio.txt", "w") as file:
        file.write(str(x))

    return FileResponse("relatorio.txt", media_type='application/octet-stream')
