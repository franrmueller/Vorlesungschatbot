import uvicorn
from fastapi import FastAPI
import logging
import os
from app.api import auth
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.callbacks.base import BaseCallbackHandler
from langchain.vectorstores.neo4j_vector import Neo4jVector
from streamlit.logger import get_logger


url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
ollama_base_url = os.getenv("OLLAMA_BASE_URL")
embedding_model_name = os.getenv("EMBEDDING_MODEL", "SentenceTransformer" )
llm_name = os.getenv("LLM", "llama2")
url = os.getenv("NEO4J_URI")

os.environ["NEO4J_URL"] = url

logger = get_logger(__name__)

embeddings, dimension = load_embedding_model(
    embedding_model_name, config={"ollama_base_url": ollama_base_url}, logger=logger
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
# Create the FastAPI application instance
app = FastAPI(
    title="Classroom Chatbot API",
    description="API endpoints for managing classes, documents, and chatting.",
    version="0.1.0",
)

# --- Placeholder: Load Models on Startup (More advanced methods exist) ---
# In a real app, use lifespan events or dependency injection for robust loading
# For now, just log that we *would* load models here.
logger.info("FastAPI app starting up...")
logger.info(f"Configured Neo4j URI: {NEO4J_URI}")
logger.info(f"Configured Ollama Base URL: {OLLAMA_BASE_URL}")

# --- API Routers (Import and include routers from app/api/* modules) ---
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(professor.router, prefix="/professor", tags=["Professor"])
app.include_router(student.router, prefix="/student", tags=["Student"])

# --- Basic Root Endpoint ---
@app.get("/")
async def read_root():
    """
    Simple health check / welcome endpoint.
    """
    logger.info("Root endpoint '/' accessed.")
    return {"message": "Welcome to the Classroom Chatbot API"}

# --- Allow running directly with python app/main.py for local dev ---
if __name__ == "__main__":
    logger.info("Running Uvicorn server directly for development...")
    # For development, reload=True is useful. Port 8000 is common.
    # Make sure this port is exposed in your Dockerfile and docker-compose.yml
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)