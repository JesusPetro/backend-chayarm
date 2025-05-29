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