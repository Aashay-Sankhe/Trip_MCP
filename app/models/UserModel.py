from sqlalchemy import Column, Integer, String, ForeignKey
from app.database_init import Base
from sqlalchemy.orm import relationship

class PlannedTrips(Base):
    __tablename__ = "planned_trips"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    budget = Column(Integer, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="trips")



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)

    trips = relationship("PlannedTrips", back_populates="user")

    