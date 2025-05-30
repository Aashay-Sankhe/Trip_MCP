from fastapi import FastAPI
from app.database_init import engine
from app.models import Base
from app.routers.BlogRoute import router as blog_router
from app.routers.UserRoute import router as user_router
from app.auth.AuthRouter import router as auth_router
from app.mcp.MCP_Request_Schema import Query
from app.mcp.client import agent_instance
import traceback
import os
from dotenv import load_dotenv, dotenv_values


app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.post("/")
async def query(query: Query):
    agent = None
    try:
        agent = await agent_instance()
        result = await agent.run(query.query)
        return {"result": result}
    except Exception as e:
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"Error details: {error_details}")
        return error_details
    finally:
        if agent is not None:
            await agent.client.close_all_sessions()


app.include_router(blog_router)
app.include_router(user_router)
app.include_router(auth_router)


# fastmcp run app/mcp/servers/travel.py -t sse -p 3001
#uvicorn app.main:app --reload
#Find ONE Home2suites hotel in New Brunswick NJ with the highest rating

"""
drop database tables:

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

"""