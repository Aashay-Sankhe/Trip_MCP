from app.database_init import get_db
from app.models.UserModel import User, PlannedTrips
from app.schemas.UserSchema import UserCreateSchema, UserLoginSchema
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.auth.AuthKeys import bcrypt_context, oauth2_bearer
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from jose import jwt, JWTError
from datetime import datetime, timezone
from app.auth import AuthKeys
from app.schemas.UserSchema import PlannedTripsCreate


def create_hashed_user(request: UserCreateSchema, db: Session = Depends(get_db)):
    new_user = User(name=request.name, email=request.email, hashed_password=bcrypt_context.hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(request: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    check = bcrypt_context.verify(request.password, user.hashed_password)
    if not check: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    return user

def create_access_token(email: str, id:int, expires_delta: timedelta):
    encode = {'sub': email, 'id': id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, AuthKeys.SECRET_KEY, algorithm=AuthKeys.ALGORITHM)

    



def login_for_access(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data, db)

    token = create_access_token(user.email, user.id, expires_delta=timedelta(minutes=30))
    
    return {'access_token': token, 'token_type': 'Bearer'}

def get_current_user(token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, AuthKeys.SECRET_KEY, algorithms=[AuthKeys.ALGORITHM])
        email = payload.get('sub')
        payload_id = payload.get('id')
        if not email or not payload_id: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        user = db.query(User).filter(User.id == payload_id).first()
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
def update_user_trip(trip_id: int, request: PlannedTripsCreate, token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    if not user: raise HTTPException(status_code=404, detail="User not found")

    user_trips = user.trips
    trip_to_update = None
    trip_found = False
    for trip in user_trips:
        if trip.id == trip_id:
            trip_to_update = trip
            trip_found = True
            break

    if not trip_found: raise HTTPException(status_code=404, detail="Trip not found")

    trip_to_update.name = request.name
    trip_to_update.description = request.description
    trip_to_update.budget = request.budget
    db.commit()
    db.refresh(trip_to_update)
    return trip_to_update