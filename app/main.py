from fastapi import FastAPI
from app.database_init import engine
from app.models import Base
from app.routers.BlogRoute import router as blog_router
from app.routers.UserRoute import router as user_router

app = FastAPI()

# Create all tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(blog_router)
app.include_router(user_router)

#uvicorn app.main:app --reload