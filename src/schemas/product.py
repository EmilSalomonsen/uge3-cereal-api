from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId  # Tilføj denne import

class ProductBase(BaseModel):
    name: str
    mfr: str
    type: str
    calories: int
    protein: float
    fat: float
    sodium: int
    fiber: float
    carbo: float
    sugars: float
    potass: int
    vitamins: int
    shelf: int
    weight: float
    cups: float
    rating: float

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }