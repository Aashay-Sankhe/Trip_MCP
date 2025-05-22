from pydantic import BaseModel
from typing import List

class PlannedTripsCreate(BaseModel):
    name: str
    description: str
    budget: int
    user_id: int

class PlannedTripsResponse(BaseModel):
    name: str
    description: str
    budget: int 

    class Config:
        from_attributes = True

class UserCreateSchema(BaseModel):
    name: str
    email: str
    password: str
    trips: List[PlannedTripsResponse] = []
    
class UserReturn(BaseModel):
    name: str
    email: str
    trips: List[PlannedTripsResponse]
    
    class Config:
        from_attributes = True
