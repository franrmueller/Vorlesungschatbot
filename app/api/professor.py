# app/api/professor.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
# Import dependencies for authorization and services later
# from app.core import security
# from app.models import user as user_models, class_ as class_models
# from app.services import class_service

router = APIRouter()

# Dependency to check if the user is a professor (example)
# async def get_current_professor_user(user: user_models.User = Depends(security.get_current_active_user)):
#     if user.role != "PROFESSOR":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
#     return user

@router.post("/classes", status_code=status.HTTP_201_CREATED)
# async def create_class(class_data: class_models.ClassCreate, professor: user_models.User = Depends(get_current_professor_user)):
async def create_class():
    """
    Professor endpoint to create a new class they teach.
    Requires PROFESSOR role.
    """
    # TODO: Add dependency injection to verify user role is PROFESSOR
    # TODO: Implement logic using class_service to create a class linked to the professor
    return {"message": "Professor: Create class placeholder - requires PROFESSOR role"}

@router.get("/classes")
# async def list_my_classes(professor: user_models.User = Depends(get_current_professor_user)):
async def list_my_classes():
    """
    Professor endpoint to list the classes they teach.
    Requires PROFESSOR role.
    """
    # TODO: Add dependency injection to verify user role is PROFESSOR
    # TODO: Implement logic to fetch classes taught by this professor
    return {"message": "Professor: List my classes placeholder - requires PROFESSOR role"}

@router.post("/upload_pdf/{class_uuid}")
# async def upload_pdf_to_class(
#     class_uuid: str,
#     pdf_file: UploadFile = File(...),
#     professor: user_models.User = Depends(get_current_professor_user)
# ):
async def upload_pdf_to_class(class_uuid: str):
     """
     Professor endpoint to upload a PDF to a specific class they teach.
     Requires PROFESSOR role.
     """
     # TODO: Add dependency injection to verify user role is PROFESSOR
     # TODO: Verify professor teaches this class_uuid
     # TODO: Implement file handling logic (saving temp, processing)
     # TODO: Call RAG service/loader to process and index the PDF chunks in Neo4j,
     #       linking them to this class_uuid and the professor.
     return {"message": f"Professor: Upload PDF placeholder for class {class_uuid} - requires PROFESSOR role"}

# Add other professor endpoints (e.g., delete class, delete PDF)