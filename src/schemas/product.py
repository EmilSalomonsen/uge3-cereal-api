from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class ProductBase(BaseModel):
    name: str
    mfr: str
    type: str
    calories: int
    protein: int
    fat: int
    sodium: int
    fiber: float
    carbo: float
    sugars: int
    potass: int
    vitamins: int
    shelf: int
    weight: float
    cups: float
    rating: float
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: str

    @classmethod
    def from_mongo(cls, data: dict):
        """Konverterer MongoDB dokument til ProductResponse model"""
        if data.get("_id"):
            # Lav en kopi af data så vi ikke modificerer originalen
            response_data = data.copy()
            # Konverter _id til id
            response_data["id"] = str(data["_id"])
            del response_data["_id"]
            # Tilføj image_url hvis det ikke findes
            if "image_url" not in response_data:
                response_data["image_url"] = f"/api/products/{response_data['id']}/image"
            return cls(**response_data)
        return cls(**data)

    class Config:
        json_encoders = {
            ObjectId: str
        }