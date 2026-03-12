from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "cache_bust": datetime.now().timestamp()})


@router.get("/clear")
def clear_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "cache_bust": datetime.now().timestamp()})
