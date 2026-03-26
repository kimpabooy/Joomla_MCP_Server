from dotenv import load_dotenv
from fastmcp import FastMCP
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.config.logging_config import configure_logging
from src.routes.chat_router import router as chat_router
import uvicorn


# Configure the logging system.
configure_logging()

# Load environment variables from .env if it exists.
load_dotenv()

# Create FastAPI app with MCP's lifespan and include routers
# Skapa MCP-app från valfri av de importerade modulerna
mcp = FastMCP("Joomla MCP Server")
mcp_app = mcp.http_app()

# Skapa FastAPI-app och inkludera MCP:s lifespan för att hantera start och stopp av MCP-servern.
app = FastAPI(lifespan=mcp_app.lifespan)

# Mount static files and include the chat router.
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(chat_router)

# Mount the MCP server on /mcp (handles SSE and streamable HTTP).
app.mount("/mcp", mcp_app)

# Run the app with Uvicorn.
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
