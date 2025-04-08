import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import logging
import os
from app.api import auth
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.vectorstores import Neo4jVector


url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
ollama_base_url = os.getenv("OLLAMA_BASE_URL")
embedding_model_name = os.getenv("EMBEDDING_MODEL", "SentenceTransformer" )
llm_name = os.getenv("LLM", "llama2")
url = os.getenv("NEO4J_URI")

os.environ["NEO4J_URL"] = url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization --
app = FastAPI(
    title="Classroom Chatbot API",
    description="API endpoints for managing classes, documents, and chatting.",
    version="0.1.0",
)


templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# --- API Routers (Import and include routers from app/api/* modules) ---
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
#app.include_router(admin.router, prefix="/admin", tags=["Admin"])
#app.include_router(professor.router, prefix="/professor", tags=["Professor"])
#app.include_router(student.router, prefix="/student", tags=["Student"])

# --- Frontend Routes ---
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

# --- Allow running directly with python app/main.py for local dev ---
if __name__ == "__main__":
    logger.info("Running Uvicorn server directly for development...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)