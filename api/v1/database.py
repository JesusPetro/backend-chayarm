from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from database import *

router = APIRouter(
    prefix="/database",
    tags=["db"],
    responses={404: {"description": "Fallo conexion"}}
)



@router.get('/getHistory', tags = ['History'])
async def get_table(select: Optional[str] = '*'): 
    return supabase.table('assembly_records').select(select).execute().data

@router.post('/potsHistory', tags=['History'])
async def post_History(data: History):
    response = supabase.table("assembly_records") \
                       .insert(data.model_dump()) \
                       .execute()
    return response.data

@router.get("/get/instruction", tags = ['Kinematics'])
async def get_angles(instruction: Optional[str] = '', select: Optional[str] = 'angles'):
  return supabase.table('instructions').select(select).execute().data[0]

@router.get("/get_instruction/", tags=['kinematics'])
async def get_angles_by_id(instruction: Optional[str] = 'search_body_a', select: Optional[str] = 'angles'):
   return supabase.table('instructions').select(select).like('command',instruction).execute().data