import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api import auth


# FastAPI App Initialization
app = FastAPI(
    title="Vorlesungschatbot API",
    description="API endpoints for managing classes, documents, and chatting.",
    version="0.1.0",
)

# API Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
#app.include_router(admin.router, prefix="/admin", tags=["Admin"])
#app.include_router(professor.router, prefix="/professor", tags=["Professor"])
#app.include_router(student.router, prefix="/student", tags=["Student"])


# Frontend Static Files and Templates
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Frontend Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Render the login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Render the registration page"""
    return templates.TemplateResponse("register.html", {"request": request})