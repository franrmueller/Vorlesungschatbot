# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # Use standard form for login
from app.models import user as user_models
from app.services import auth_service
from app.core import security
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/register", response_model=user_models.User, status_code=status.HTTP_201_CREATED)
async def register_student(user_data: user_models.UserCreate):
    """
    Endpoint for student self-registration.
    """
    logger.info(f"Attempting registration for user: {user_data.username}")
    # Ensure role is STUDENT for self-registration if not explicitly set otherwise
    if not user_data.role or user_data.role.upper() != "STUDENT":
        user_data.role = "STUDENT" # Enforce student role for this endpoint

    new_user = await auth_service.create_user(user_data=user_data)
    if not new_user:
        logger.warning(f"Registration failed for {user_data.username}, likely username exists.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered or error during creation."
        )
    logger.info(f"User {new_user.username} registered successfully.")
    # Return the created user details (excluding password hash)
    return new_user

@router.post("/login/token", response_model=user_models.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint for user login, returns JWT access token.
    Uses standard OAuth2 form data (username, password).
    """
    logger.info(f"Login attempt for user: {form_data.username}")
    user = await auth_service.authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if not user:
        logger.warning(f"Login failed for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    access_token = security.create_access_token(
        data={"sub": user.username, "role": user.role} # Include role in token payload
    )
    logger.info(f"Login successful for user: {form_data.username}. Token issued.")
    return {"access_token": access_token, "token_type": "bearer"}

# Example Protected Route (add to student.py or professor.py later)
# @router.get("/users/me", response_model=user_models.User)
# async def read_users_me(current_user: user_models.User = Depends(security.get_current_active_user)):
#     """ Fetches details for the currently authenticated user. """
#     # Note: get_current_active_user needs modification to return full User model from DB
#     # For now, it returns a dict. This endpoint would fail until get_current_active_user is fixed.
#     return current_user