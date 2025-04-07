from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
import os
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# --- JWT Token Handling ---
# Load from environment variables (use strong secrets!)
SECRET_KEY = os.getenv("SECRET_KEY", "your-very-secret-key-for-jwt-please-change")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

if SECRET_KEY == "your-very-secret-key-for-jwt-please-change":
    print("WARNING: Using default JWT SECRET_KEY. Please set a strong secret key in your environment.")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/token") # Matches the login endpoint path

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Dependency for Getting Current User (Placeholder for DB logic) ---
# This needs to interact with your database service later
async def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    """
    Decodes JWT token, validates it, and retrieves user information.
    This is a dependency used by protected endpoints.
    It needs to be expanded to fetch the full user object from the DB.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        token_data = {"username": username, "role": role} # Simplification for now
        # TODO: Replace below with DB lookup using username from token_data
        # user = await auth_service.get_user_by_username(username=username)
        # if user is None:
        #     raise credentials_exception
        # For now, just return the decoded data (INSECURE - MUST FETCH FROM DB)
        print(f"WARNING: Returning mock user from token: {token_data}. MUST implement DB lookup.")
        return token_data # Replace with actual user object from DB
    except JWTError:
        raise credentials_exception

# Placeholder for active user check (can be expanded)
async def get_current_active_user(current_user: dict = Depends(get_current_user_from_token)):
    # TODO: Add checks if user is active/disabled based on DB field if needed
    # if current_user.disabled: # Assuming a 'disabled' field on the user model
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user