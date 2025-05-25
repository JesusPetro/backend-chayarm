import time

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute
from api import *
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origin = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials = True,
    allow_origins = origin, 
    allow_methods = ['*']
)

value_prueba = [
  {
    "id": 1743372198446,
    "head": "#FFD700",
    "legs": "#FFD700",
    "timestamp": "2025-03-30T22:03:18.446Z"
  },
  {
    "id": 1743372191131,
    "head": "#FF6347",
    "legs": "#FF6347",
    "timestamp": "2025-03-30T22:03:11.131Z"
  }
]

app.include_router(esp32.router)

@app.get("/", tags=["Hola"])
async def not_timed():
    return {"message": "Not timed"}


