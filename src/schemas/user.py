from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

# Basis brugermodel med fælles felter
class UserBase(BaseModel):
    email: EmailStr
    username: str

# Model til oprettelse af ny bruger
class UserCreate(UserBase):
    password: str  # Password gemmes aldrig direkte i databasen

# Model til at sende brugerdata tilbage til klienten
class UserResponse(BaseModel):
    email: str
    username: str
    id: str

    @classmethod
    def from_mongo(cls, data: dict):
        """Konverterer MongoDB dokument til UserResponse model"""
        if data.get("_id"):
            data["id"] = str(data["_id"])
            del data["_id"]
        if "hashed_password" in data:  # Fjern password før data sendes til klient
            del data["hashed_password"]
        return cls(**data)

    class Config:
        json_encoders = {
            ObjectId: str  # Konverterer MongoDB ObjectId til string
        }

# Model til login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Model til JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"  # Standard token type for JWT