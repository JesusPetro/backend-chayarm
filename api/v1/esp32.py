import serial
from services import *
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import json

router = APIRouter(
    prefix="/esp32",
    tags=["Esp32"],
    responses={404: {"description": "Fallo conexion"}}
)

class Roblox(BaseModel):
    head: str
    body: str


def conexion():
    serialConnection = Conexion()
    try:
        serialConnection.open_connection()
        yield serialConnection
    finally:
        serialConnection.cerrar()


@router.get("/command/{mensaje}")
async def send_command(mensaje: str, serial_connection: serial.Serial = Depends(conexion)):
    try:
        serial_connection.enviar_mensaje(mensaje)
        value = serial_connection.recibir_mensaje()
        serial_connection.cerrar()
        return value
    except Exception as e:
        return e


@router.get("/")
async def send_figure(head: Optional[str] = None, body: Optional[str] = None, serial_connection: serial.Serial = Depends(conexion)):
    head_colors = {
    "D3D3D3": "h1",
    "FFD700": "h2",
    "FF6347": "h3",
  };
    
    body_colors = {
    "D3D3D3": "l1",
    "FFD700": "l2",
    "FF6347": "l3",
    }
    
    sphead, spbody = head_colors[head], body_colors[body]

    try: 
        serial_connection.enviar_mensaje(sphead + " " + spbody)
        value = serial_connection.recibir_mensaje()
        return value
    except Exception as e:
        return e
    finally:
        serial_connection.cerrar()
        # return {"message": "Item replaced",  "roblox": {'head': head_colors[head], 'body': body_colors[body]}}