from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.routes.mcp import router as mcp_router
from src.routes.views import router as views_router
import uvicorn

# Ladda miljövariabler från .env om den finns
from dotenv import load_dotenv
load_dotenv()

# Skapa FastAPI app och inkludera routrar
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(mcp_router)
app.include_router(views_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
