from dotenv import load_dotenv
from fastmcp import FastMCP
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.config.logging_config import configure_logging
from src.routes.chat_router import router as chat_router
from starlette.middleware.sessions import SessionMiddleware
import secrets
import uvicorn


# Configure the logging system.
configure_logging()

# Load environment variables from .env if it exists.
load_dotenv()

# Create FastAPI app with MCP's lifespan and include routers
mcp = FastMCP("Joomla MCP Server")
mcp_app = mcp.http_app()

# Create FastAPI-app and include MCP's lifespan for managing MCP server lifecycle.
app = FastAPI(lifespan=mcp_app.lifespan)

# Add session middleware for managing user sessions in the chat interface.
# The secret key is generated securely using secrets.token_hex(16) to ensure session data integrity and security.
# The key is generated at runtime, which means sessions will be lost on server restart, but this is acceptable for our use case.
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(16))

# Add middleware, routes, and other FastAPI configurations here if needed.

# Mount static files and include the chat router.
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(chat_router)

# Mount the MCP server on /mcp (handles SSE and streamable HTTP).
app.mount("/mcp", mcp_app)

# Run the app with Uvicorn.
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
