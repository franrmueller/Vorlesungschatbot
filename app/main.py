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

@app.get("/student_class", response_class=HTMLResponse)
async def student_class_page(request: Request):
    """Render the registration page"""
    return templates.TemplateResponse("student_class.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Render the registration page"""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/admin/dashboard", response_class=HTMLResponse)

async def admin_dashboard(request: Request):

    return templates.TemplateResponse("admin_dashboard.html", {"request": request})
 
@app.get("/admin/professors", response_class=HTMLResponse)

async def admin_professors(request: Request):

    return templates.TemplateResponse("admin_professors.html", {"request": request})
 
@app.get("/admin/classes", response_class=HTMLResponse)

async def admin_classes(request: Request):

    return templates.TemplateResponse("admin_classes.html", {"request": request})
 
@app.get("/admin/students", response_class=HTMLResponse)

async def admin_students(request: Request):

    return templates.TemplateResponse("admin_students.html", {"request": request})
 
@app.get("/admin/pdf", response_class=HTMLResponse)

async def admin_pdf(request: Request):

    return templates.TemplateResponse("admin_pdf.html", {"request": request})
 
@app.get("/admin/chathistory", response_class=HTMLResponse)

async def admin_chathistory(request: Request):

    return templates.TemplateResponse("admin_chathistory.html", {"request": request})
 
@app.get("/professor/classes", response_class=HTMLResponse)

async def professor_classes(request: Request):

    return templates.TemplateResponse("professor_classes.html", {"request": request})
 
@app.get("/professor/pdf/{course_id}", response_class=HTMLResponse)

async def professor_pdf(request: Request, course_id: str):

    return templates.TemplateResponse("professor_pdf.html", {"request": request, "course_id": course_id})
 
@app.get("/student/classes", response_class=HTMLResponse)

async def student_classes(request: Request):

    return templates.TemplateResponse("student_class.html", {"request": request})
 
@app.get("/chat/{course_id}", response_class=HTMLResponse)

async def chat_view(request: Request, course_id: str):

    return templates.TemplateResponse("chat.html", {"request": request, "course_id": course_id})

 