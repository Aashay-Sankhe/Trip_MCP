from typing import List
from fastapi import APIRouter, Depends, status
from app.crud.UserCrudOps import get_all, update_user, delete_user, add_plan, get_user_plans, get_one_user
from app.database_init import get_db
from app.schemas.UserSchema import UserCreateSchema, UserReturn, PlannedTripsResponse, PlannedTripsCreate
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.post("/{id}/trips", response_model = PlannedTripsResponse, status_code=status.HTTP_201_CREATED)
def add_trip_to_user(id: int, request: PlannedTripsCreate, db: Session = Depends(get_db)):
    return add_plan(id, request, db)

@router.get("/{id}/trips", response_model=List[PlannedTripsResponse])
def get_user_trips(id: int, db: Session = Depends(get_db)):
    return get_user_plans(id, db)

@router.get("/", response_model=List[UserReturn])
def get_all_users(db: Session = Depends(get_db)):
    return get_all(db)



@router.put("/{id}", response_model=UserReturn, status_code=status.HTTP_202_ACCEPTED)
def update_existing_user(id: int, request: UserCreateSchema, db: Session = Depends(get_db)):
    return update_user(id, request, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(id: int, db: Session = Depends(get_db)):
    return delete_user(id, db)


@router.get("/{id}", response_model=UserReturn)
def get_one_user_info(id:int, db: Session = Depends(get_db)):
    return get_one_user(id, db)