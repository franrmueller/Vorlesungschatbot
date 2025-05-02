# app/api/student.py
from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.core.dependencies import get_current_student_user
from app.services.class_service import get_enrolled_classes # type: ignore
# Import dependencies for authorization and services later
# from app.core import security
# from app.models import user as user_models, chat as chat_models
# from app.services import class_service, chat_service
# from fastapi.responses import StreamingResponse # For streaming chat responses

router = APIRouter()

# Dependency to check if the user is a student (example)
# async def get_current_student_user(user: user_models.User = Depends(security.get_current_active_user)):
#     if user.role != "STUDENT":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
#     return user

@router.post("/enroll/{enrollment_code}")
# async def enroll_in_class(enrollment_code: str, student: user_models.User = Depends(get_current_student_user)):
async def enroll_in_class(enrollment_code: str):
    """
    Student endpoint to enroll in a class using an enrollment code.
    Requires STUDENT role.
    """
    # TODO: Add dependency injection to verify user role is STUDENT
    # TODO: Implement logic using class_service to find class by code and create ENROLLED_IN relationship
    return {"message": f"Student: Enroll in class placeholder for code {enrollment_code} - requires STUDENT role"}

@router.get("/classes")
#async def list_my_enrolled_classes(request: Request, student: dict = Depends(get_current_student_user)):
#    courses = get_enrolled_classes(student["username"])
#    return template.TemplateResponse("student_classes.html", {
#        "request": request,
#        "courses": courses  #Wird an Template übergeben
#    })

# async def list_my_enrolled_classes():
#"""
    # Student endpoint to list classes they are enrolled in.
  #  Requires STUDENT role.
 #   """
    # TODO: Add dependency injection to verify user role is STUDENT
    # TODO: Implement logic to fetch classes the student is enrolled in
 #   return {"message": "Student: List enrolled classes placeholder - requires STUDENT role"}

@router.post("/chat/{class_uuid}")
# async def chat_with_class_docs(
#     class_uuid: str,
#     chat_request: chat_models.ChatRequest, # Use Pydantic model for request body
#     student: user_models.User = Depends(get_current_student_user)
# ):
async def chat_with_class_docs(class_uuid: str):
     """
     Student endpoint to ask a question about documents in a specific class.
     Requires STUDENT role.
     """
     # TODO: Add dependency injection to verify user role is STUDENT
     # TODO: Verify student is enrolled in class_uuid
     # TODO: Implement logic using chat_service:
     #      - Get query from chat_request.query
     #      - Run the RAG chain scoped to class_uuid
     #      - Return the response (potentially using StreamingResponse)
     return {"message": f"Student: Chat placeholder for class {class_uuid} - requires STUDENT role"}