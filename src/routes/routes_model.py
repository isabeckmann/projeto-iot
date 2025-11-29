from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import os
from src.controllers.sensor_controller import (
    save_sensor_data,
    list_sensor_data,
    list_by_sensor,
    get_latest_data,
    delete_record,
    register_sensor,
    get_grouped_data
)
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
security = HTTPBearer()

# Get token from environment variable
API_TOKEN = os.getenv("AUTH_TOKEN", "your-default-token")

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials.credentials

class SensorInput(BaseModel):
    sensorId: str
    type: str
    value: float
    timestamp: str

class SensorRegister(BaseModel):
    sensorId: str
    type: str
    location: str

# Protected routes - require token
@router.post("/sensor/data", dependencies=[Depends(verify_token)])
def receive_data(data: SensorInput):
    return save_sensor_data(data)

@router.get("/sensor/data", dependencies=[Depends(verify_token)])
def get_all():
    return list_sensor_data()

# Últimos registros de cada sensor
@router.get("/sensor/data/latest", dependencies=[Depends(verify_token)])
def get_latest():
    return get_latest_data()

# Agrupar dados por sensor
@router.get("/sensor/data/grouped", dependencies=[Depends(verify_token)])
def get_grouped():
    return get_grouped_data()

# Dados por ID do sensor
@router.get("/sensor/data/{sensorId}", dependencies=[Depends(verify_token)])
def get_by_sensor(sensorId: str):
    return list_by_sensor(sensorId)

# Remover um registro específico
@router.delete("/sensor/data/{record_id}", dependencies=[Depends(verify_token)])
def delete_sensor_record(record_id: int):
    return delete_record(record_id)

# Cadastrar sensores manualmente
@router.post("/sensor/register", dependencies=[Depends(verify_token)])
def create_sensor(sensor: SensorRegister):
    return register_sensor(sensor)