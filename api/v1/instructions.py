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
        'close_v2': 'close_gripperv2',
        'close': 'close_gripper'
    },
    'neutral': 'neutral_position',
    'neutral_final': 'final_position'
}

neutral = get_instruction_angles(instruction=commands['neutral'])
final_neutral = get_instruction_angles(instruction=commands['neutral_final'])
gripper_close = get_instruction_angles(instruction=commands['gripper']['close'])
gripper_open = get_instruction_angles(instruction=commands['gripper']['open'])
gripper_closev2 = get_instruction_angles(instruction=commands['gripper']['close_v2'])
    

@router.get('/stept_assemble/')
async def get_steps_to_assemble(head: Optional[str] = 'white', body: Optional[str] = 'white', leg: Optional[str] = 'white'):
    
    steps = [] + final_neutral
    steps += get_instruction_angles(instruction=commands['leg']['search'][leg])   + gripper_closev2 + neutral + get_instruction_angles(instruction=commands['leg']['put'])  + gripper_open
    steps += neutral + [{'angles': {'q5': 90}}]
    steps += get_instruction_angles(instruction=commands['body']['search'][body]) + gripper_closev2 
    
    if body == 'blue':
        steps += [{'angles': {'q3': 102}}]

    steps += neutral + get_instruction_angles(instruction=commands['body']['put']) + gripper_open
    steps += [{'angles': {'q2': 90, 'q5': 90}}] + [{'angles': {'q3': 90}}]
    steps += get_instruction_angles(instruction=commands['head']['search'][head]) + gripper_close + neutral + get_instruction_angles(instruction=commands['head']['put']) + gripper_open
    
    steps += final_neutral
    return steps

