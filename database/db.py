#TODO: aqui va la lógica de la influxdb o supabase

from supabase import create_client
from pydantic import BaseModel

SUPABASE_URL = 'https://oiawxmuebjueqlchwxie.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9pYXd4bXVlYmp1ZXFsY2h3eGllIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODUzNjA1NCwiZXhwIjoyMDY0MTEyMDU0fQ.DLFnDhfRTTxT11hv0Httcwn4g_KG_YVrKyJK40igjuo'


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class History(BaseModel):
    head: str
    torso: str
    legs: str

def conexion_db():
    return supabase.table('assembly_records').select('*').execute().data

def get_instruction_angles(instruction: str = 'search_body_a%', select: str = 'angles'):
   return supabase.table('instructions').select(select).like('command',instruction).execute().data

if __name__ == "__main__":
    print(conexion_db())