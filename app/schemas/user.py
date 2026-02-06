from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    nom: str = Field(..., min_length=1, max_length=100)
    prenom: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True
    type: str = Field(..., description="Type of user: administrateur, medecin, secretaire, visualiseur")

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    # Optional fields for specific roles
    matricule: Optional[str] = None
    specialite: Optional[str] = None
    desk_number: Optional[str] = None
    department_access: Optional[str] = None

# Properties to receive via API on update
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    
    # Optional fields for specific roles
    matricule: Optional[str] = None
    specialite: Optional[str] = None
    desk_number: Optional[str] = None
    department_access: Optional[str] = None

# Properties to return to client
class UserResponse(UserBase):
    id: int
    uuid: UUID
    created_at: datetime
    updated_at: datetime
    
    # Specific fields
    matricule: Optional[str] = None
    specialite: Optional[str] = None
    desk_number: Optional[str] = None
    department_access: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
