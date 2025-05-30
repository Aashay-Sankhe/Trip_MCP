from typing import List
from fastapi import APIRouter, Depends, status
from app.database_init import get_db
from app.schemas.UserSchema import UserCreateSchema, UserReturn
from sqlalchemy.orm import Session
from app.auth.AuthCrudOps import create_hashed_user, login_for_access, get_current_user
from app.auth.TokenSchema import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.AuthKeys import oauth2_bearer

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)



@router.post("/", response_model=UserReturn, status_code=status.HTTP_201_CREATED)
def create_new_user(request: UserCreateSchema, db: Session = Depends(get_db)):
    return create_hashed_user(request, db)

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_for_access(form_data, db)

@router.get("/{id}", response_model=UserReturn)
def get_logged_in_user(token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)):
    return get_current_user(token, db)

''' AUTHENTICATED USER ROUTES BELOW, UNCOMMENT TO USE'''

'''


@router.put("/user/trips/{trip_id}", response_model=PlannedTripsResponse)
def update_user_plan(trip_id: int, request: PlannedTripsCreate, token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)):
    return update_user_trip(trip_id, request, token, db)

@router.put("/user", response_model=UserReturn)
def update_user_info(request: UserCreateSchema, token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)):
    return update_user(request, token, db)

@router.post("/user/trips", response_model=PlannedTripsResponse)
def add_user_trip(request: PlannedTripsCreate, token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)):
    return add_user_trip(request, token, db)
'''