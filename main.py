from dotenv import load_dotenv
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.routes.chat_router import router as chat_router
from src.routes.views import router as views_router
from src.tools.mcp_tools import mcp
import uvicorn

# Konfigurera loggning
logging.basicConfig(level=logging.INFO)

# Ladda miljövariabler från .env om den finns
load_dotenv()

# Skapa MCP ASGI-app och hämta dess lifespan
mcp_app = mcp.http_app()

# Skapa FastAPI app med MCP:s lifespan och inkludera routrar
app = FastAPI(lifespan=mcp_app.lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(chat_router)
app.include_router(views_router)

# Montera FastMCP-servern på /mcp (hanterar SSE och streamable HTTP)
app.mount("/mcp", mcp_app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
