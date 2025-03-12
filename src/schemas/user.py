from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel):
    email: str
    username: str
    id: str

    @classmethod
    def from_mongo(cls, data: dict):
        if data.get("_id"):
            data["id"] = str(data["_id"])
            del data["_id"]
        if "hashed_password" in data:
            del data["hashed_password"]
        return cls(**data)

    class Config:
        json_encoders = {
            ObjectId: str
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"