from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user

# Role-based dependencies for user authorization 
# STUDENT-only Zugriff
async def get_current_student_user(user: dict = Depends(get_current_user)):
    if user["role"] != "STUDENT":
        raise HTTPException(status_code=403, detail="Nur für Studenten erlaubt.")
    return user

# PROFESSOR-only Zugriff
async def get_current_professor_user(user: dict = Depends(get_current_user)):
    if user["role"] != "PROFESSOR":
        raise HTTPException(status_code=403, detail="Nur für Professoren erlaubt.")
    return user


#TODO: Admin Zugriff
