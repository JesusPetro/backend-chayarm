import time

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute
from api import *
from services.kInversa import KInverse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origin = [
    'http://localhost:5173',
    'https://hmi-chayarm-c9iqr11sb-gsus-projects-b0d1512e.vercel.app',
    'https://hmi-chayarm.vercel.app',
    'https://hmi-chayarm-gsus-projects-b0d1512e.vercel.app'
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

app.include_router(database.router)
app.include_router(esp32.router)

@app.get("/", tags=["Hola"])
async def not_timed():
    return {"message": "Not timed"}


@app.get("/prueba", tags =['test'])
async def test():
    return {'message': "Este mensaje es de prueba"}


@app.post("/prueba", tags=['test'])
async def post_test(txt: str):
  return {'message': f'Este mensaje es de prueba y esto posteaste: {txt}'}

@app.get("/prueba/kInverse", tags= ['test'])
async def test_k(x: float,y: float, z: float):
  intento = KInverse()
  return intento.Inter(x,y,z)
  
@app.get('/validacion')
async def validacion_cv():
   return 'Correcto'