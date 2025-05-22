from app.database_init import get_db
from app.models.UserModel import User, PlannedTrips
from app.schemas.UserSchema import UserCreateSchema, PlannedTripsCreate
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException



def get_all(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

def get_one_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    return user

def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return "User deleted successfully"



def update_user(id: int, request: UserCreateSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    
    user.name = request.name
    user.email = request.email
    user.hashed_password = request.password
    db.commit()
    db.refresh(user)
    return user



def delete_all(db: Session = Depends(get_db)):
    db.query(User).delete()
    db.commit()
    return "All users deleted successfully"

def add_plan(id: int, request: PlannedTripsCreate, db: Session = Depends(get_db)):
    user_to_add_to = db.query(User).filter(User.id == id).first();
    if not user_to_add_to: raise HTTPException(status_code=404, detail="User not found")
    new_trip = PlannedTrips(name=request.name, description = request.description, budget = request.budget, user_id = id)
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip

def get_user_plans(id: int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    return user.trips

