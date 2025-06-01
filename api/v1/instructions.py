from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from database import *

router = APIRouter(
    prefix="/instructions",
    tags=["instr"],
    responses={404: {"description": "Fallo conexión - instr"}}
)

commands = {
    'head': {
        'search': {
            'white': 'search_head_a',
            'blue': 'search_head_b',
            'red': 'search_head_c'
        },
        'put': 'put_head'
    },
    'body': {
        'search': {
            'white': 'search_body_a',
            'blue': 'search_body_b',
            'red': 'search_body_c'
        },
        'put': 'put_body'
    },
    'leg': {
        'search': {
            'white': 'search_leg_a',
            'blue': 'search_leg_b',
            'red': 'search_leg_c'
        },
        'put': 'put_leg'
    },
    'gripper': {
        'open': 'open_gripper',
        'close': 'close_gripper'
    },
    'neutral': 'neutral_position'
}

neutral = get_instruction_angles(instruction=commands['neutral'])
gripper_close = get_instruction_angles(instruction=commands['gripper']['close'])
gripper_open = get_instruction_angles(instruction=commands['gripper']['open'])
    

@router.get('/stept_assemble/')
async def get_steps_to_assemble(head: Optional[str] = 'white', body: Optional[str] = 'white', leg: Optional[str] = 'white'):
    
    steps = []
    steps += get_instruction_angles(instruction=commands['leg']['search'][leg])   + gripper_close + neutral + get_instruction_angles(instruction=commands['leg']['put'])  + gripper_open
    steps += get_instruction_angles(instruction=commands['body']['search'][body]) + gripper_close + neutral + get_instruction_angles(instruction=commands['body']['put']) + gripper_open
    steps += get_instruction_angles(instruction=commands['head']['search'][head]) + gripper_close + neutral + get_instruction_angles(instruction=commands['head']['put']) + gripper_open
    steps += neutral
    return steps

