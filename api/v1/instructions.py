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
        'put': 'put_head',
        'close_gripper': 'close_gripper_head'
    },
    'body': {
        'search': {
            'white': 'search_body_a',
            'blue': 'search_body_b',
            'red': 'search_body_c'
        },
        'put': 'put_body',
        'close_gripper': 'close_gripper_body'
    },
    'leg': {
        'search': {
            'white': 'search_leg_a',
            'blue': 'search_leg_b',
            'red': 'search_leg_c'
        },
        'put': 'put_leg',
        'close_gripper': 'close_gripper_leg'
    },
    'gripper': {
        'open': 'open_gripper'
    }
}

@router.get('/stept_assemble/')
async def get_steps_to_assemble(head: Optional[str] = 'white', body: Optional[str] = 'white', leg: Optional[str] = 'white'):
    steps = [] + get_instruction_angles(instruction=commands['head']['search'][head])
    steps += get_instruction_angles(instruction=commands['head']['close_gripper'])
    steps += get_instruction_angles(instruction=commands['body']['search'][body])
    steps += get_instruction_angles(instruction=commands['leg']['search'][leg])
    return steps

