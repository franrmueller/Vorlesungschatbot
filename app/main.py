import uvicorn
from fastapi import FastAPI
import logging
import os

# --- Configuration (Ideally move to app/core/config.py later) ---
# Load essential config needed at startup (example)
NEO4J_URI = os.getenv("NEO4J_URI")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
# Add checks or default values as needed

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
logger.info(f"Configured Neo4j URI: {NEO4J_URI}") # Be careful logging sensitive info
logger.info(f"Configured Ollama Base URL: {OLLAMA_BASE_URL}")
# llm = None
# embeddings = None
# try:
#    logger.info("Attempting to load LLM and Embedding models...")
#    # embeddings, dimension = load_embedding_model(...) # Adapt from your chains.py/utils.py
#    # llm = load_llm(...) # Adapt from your chains.py/utils.py
#    logger.info("Models loaded successfully (placeholder).")
# except Exception as e:
#    logger.error(f"FATAL: Failed to load models on startup: {e}")
    # Decide if the app should fail to start if models don't load

# --- API Routers (Import and include routers from app/api/* modules) ---
# Example: Create these files even if they are empty for now
# from app.api import auth, admin, professor, student # Create these python files in app/api/

# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(admin.router, prefix="/admin", tags=["Admin"])
# app.include_router(professor.router, prefix="/professor", tags=["Professor"])
# app.include_router(student.router, prefix="/student", tags=["Student"])

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