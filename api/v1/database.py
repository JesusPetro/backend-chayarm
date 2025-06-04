from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from database import *

router = APIRouter(
    prefix="/database",
    tags=["db"],
    responses={404: {"description": "Fallo conexion"}}
)

valores = []

@router.get('/get_pieces', tags = ['History'])
async def get_pieces():

    opc = {
        '#D3D3D3': 'white',
        '#0074D9': 'blue',
        '#FF6347': 'red'
    }

    if len(valores) > 0:
        intento = valores.pop()
        intento = {'color1': opc[intento[0]['head']], 'color2': opc[intento[0]['torso']], 'color3': opc[intento[0]['legs']]}
    else: 
        intento = []
    return intento

@router.get('/getHistory', tags = ['History'])
async def get_table(select: Optional[str] = '*'): 
    return supabase.table('assembly_records').select(select).execute().data

@router.post('/potsHistory', tags=['History'])
async def post_History(data: History):
    response = supabase.table("assembly_records") \
                       .insert(data.model_dump()) \
                       .execute()
    valores.append(response.data)
    return response.data

@router.get("/get/instruction", tags = ['Kinematics'])
async def get_angles(instruction: Optional[str] = '', select: Optional[str] = 'angles'):
  return supabase.table('instructions').select(select).execute().data[0]

@router.get("/get_instruction/", tags=['kinematics'])
async def get_angles_by_id(instruction: Optional[str] = 'search_body_a', select: Optional[str] = 'angles'):
   return supabase.table('instructions').select(select).like('command',instruction).execute().data