from fastapi import FastAPI

from auth import endpoints as auth_endpoint
from user import endpoints as user_endpoint
from item import endpoints as item_endpoint


app = FastAPI()

app.include_router(auth_endpoint.auth_router)
app.include_router(user_endpoint.user_router)
app.include_router(item_endpoint.item_router)