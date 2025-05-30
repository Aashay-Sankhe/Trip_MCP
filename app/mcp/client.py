HOST = 'http://127.0.0.1:3001'

import asyncio
import os
from dotenv import load_dotenv, dotenv_values
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient


try:
    loaded = dotenv_values(".env")
    print("Loaded .env contents:", loaded)
    load_dotenv(override=True)
except Exception as e:
    print(f"Error loading .env: {e}")




async def agent_instance():
    """Run the example using a configuration file."""
    # Load environment variables
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    if OPENAI_API_KEY: print("OPENAI_API_KEY found in environment variables")

    config = {
        "mcpServers": {
            "travel": {
                "url": f"{HOST}/sse",  # Add /sse endpoint
                "transport": "streamable-http",
                "headers": {
                    "Accept": "text/event-stream",
                    "Connection": "keep-alive"
                }
            }
        }
    }

    # Create MCPClient from config file
    client = MCPClient.from_dict(config)

    try:
        # Create LLM
        llm = ChatOpenAI(
            model="gpt-4",
            temperature=0
        )

        # Create agent with the client and server manager
        agent = MCPAgent(
            llm=llm, 
            client=client, 
            max_steps=30,
            use_server_manager=False  # Disable server manager since we have only one server
        )

        # Run the query
        '''
        result = await agent.run(
            "Find ONE Home2suites hotel in New Brunswick NJ with the highest rating",
            max_steps=30
        )
        print(f"\nResult: {result}")
        '''
        return agent
    finally:
        # Clean up all sessions
        await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(agent_instance())