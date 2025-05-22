from fastapi import FastAPI
from app.database_init import engine
from app.models import Base
from app.routers.BlogRoute import router as blog_router
from app.routers.UserRoute import router as user_router
from app.auth.AuthRouter import router as auth_router

app = FastAPI()


Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "front page or sum"}

app.include_router(blog_router)
app.include_router(user_router)
app.include_router(auth_router)



#uvicorn app.main:app --reload

"""
drop database tables:

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

"""