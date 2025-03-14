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
    image_url: Optional[str] = None  # Nyt felt, valgfrit med None som default

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: str = Field(alias="_id")

    @classmethod
    def from_mongo(cls, data: dict):
        if data.get("_id"):
            data["id"] = str(data["_id"])
            del data["_id"]
            # Tilføj image URL hvis det ikke allerede findes
            if "image_url" not in data:
                data["image_url"] = f"/api/products/{data['id']}/image"
        return cls(**data)

    class Config:
        json_encoders = {
            ObjectId: str
        }
        populate_by_name = True