from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import uuid

class UserBase(BaseModel):
    username: EmailStr
    name: Optional[str] = None
    role: str = Field(default="STUDENT", description="User role (STUDENT, PROFESSOR, ADMIN)")

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserInDBBase(UserBase):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    # We don't store password hash here directly for reading generally,
    # but the DB query needs it for authentication

class User(UserInDBBase):
    # Model for returning user data (excluding sensitive info like password hash)
    pass

    class Config:
        from_attributes = True # Replaces orm_mode=True in Pydantic v2

class UserInDB(UserInDBBase):
    # Model representing user data as stored in the database, including hashed password
    hashed_password: str

# Model for Token Data
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[EmailStr] = None
    role: Optional[str] = None