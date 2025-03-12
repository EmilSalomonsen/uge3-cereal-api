from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from ..database.connection import DatabaseConnection
from ..schemas.product import ProductResponse, ProductCreate
from bson import ObjectId
from bson.errors import InvalidId
from .auth import get_current_user

router = APIRouter()
db = DatabaseConnection().get_db()

@router.get("/products/", response_model=List[ProductResponse])
async def get_products(
    calories: Optional[int] = None,
    manufacturer: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    """Get all products with optional filtering"""
    query = {}
    if calories is not None:
        query["calories"] = calories
    if manufacturer is not None:
        query["mfr"] = manufacturer
    
    products = list(db.products.find(query).skip(skip).limit(limit))
    return [ProductResponse.from_mongo(product) for product in products]  # Konverter hver produkt

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Get a specific product by ID"""
    try:
        product = db.products.find_one({"_id": ObjectId(product_id)})
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID format")

@router.post("/products/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new product"""
    product_dict = product.model_dump()
    result = db.products.insert_one(product_dict)
    created_product = db.products.find_one({"_id": result.inserted_id})
    return ProductResponse.from_mongo(created_product)  # Konverter nyt produkt

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product: ProductCreate,
    current_user: dict = Depends(get_current_user)
):
    """Update a product"""
    try:
        product_dict = product.model_dump()
        result = db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": product_dict}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        updated_product = db.products.find_one({"_id": ObjectId(product_id)})
        return ProductResponse.from_mongo(updated_product)  # Konverter opdateret produkt
    except:
        raise HTTPException(status_code=400, detail="Invalid product ID")

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a product"""
    try:
        result = db.products.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted successfully"}
    except:
        raise HTTPException(status_code=400, detail="Invalid product ID")