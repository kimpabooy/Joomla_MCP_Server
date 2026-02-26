from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.routes.mcp import router as mcp_router
from src.routes.views import router as views_router
import uvicorn


app = FastAPI()
app.include_router(mcp_router)
app.include_router(views_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
