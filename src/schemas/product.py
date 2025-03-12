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
    id: str = Field(alias="_id")

    @classmethod
    def from_mongo(cls, data: dict):
        if data.get("_id"):
            data["id"] = str(data["_id"])
            del data["_id"]
        return cls(**data)

    class Config:
        json_encoders = {
            ObjectId: str
        }
        populate_by_name = True