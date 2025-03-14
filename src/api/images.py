from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from .auth import get_current_user
import os
from typing import List
from bson import ObjectId
from bson.errors import InvalidId
from ..database.connection import DatabaseConnection

router = APIRouter()
db = DatabaseConnection().get_db()

# Ændr sti til den eksisterende billede-mappe
UPLOAD_DIR = "data/cereal-pictures"

# Tilladte filtyper
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}

@router.get("/products/{product_id}/image")
async def get_product_image(product_id: str):
    """Hent et produkts billede"""
    try:
        # Find produktet først
        product = db.products.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # List alle filer i mappen
        files = os.listdir(UPLOAD_DIR)
        
        # Fjern mellemrum og konverter til lowercase for sammenligning
        product_name = product["name"].replace(" ", "").lower()
        
        # Print for debugging
        print(f"Søger efter produkt (uden mellemrum): {product_name}")
        
        # Søg efter filen
        for file in files:
            file_name_without_ext = os.path.splitext(file)[0].replace(" ", "").lower()
            if file_name_without_ext == product_name:
                return FileResponse(os.path.join(UPLOAD_DIR, file))
                
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    raise HTTPException(status_code=404, detail="Intet billede fundet for dette produkt")

@router.post("/products/{product_id}/image")
async def upload_product_image(
    product_id: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload et billede til et produkt"""
    try:
        product = db.products.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Tjek filtype
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Filtype ikke tilladt. Tilladte typer: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Forbered nyt filnavn
        new_file_name = f"{product['name']}{file_ext}"
        new_file_path = os.path.join(UPLOAD_DIR, new_file_name)
        
        # Slet eksisterende billeder hvis de findes
        files = os.listdir(UPLOAD_DIR)
        product_name = product["name"].replace(" ", "").lower()
        for existing_file in files:
            file_name_without_ext = os.path.splitext(existing_file)[0].replace(" ", "").lower()
            if file_name_without_ext == product_name:
                old_file_path = os.path.join(UPLOAD_DIR, existing_file)
                if old_file_path != new_file_path:  # Undgå at slette hvis samme navn
                    try:
                        os.remove(old_file_path)
                        print(f"Slettet gammelt billede: {existing_file}")
                    except Exception as e:
                        print(f"Kunne ikke slette gammelt billede {existing_file}: {e}")
                        # Fortsæt selvom vi ikke kunne slette det gamle billede
        
        # Gem det nye billede
        contents = await file.read()
        with open(new_file_path, "wb") as f:
            f.write(contents)
            
        image_url = f"/api/products/{product_id}/image"
        db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {"image_url": image_url}}
        )
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kunne ikke gemme fil: {str(e)}")
    
    return {
        "message": "Billede opdateret succesfuldt",
        "filename": new_file_name,
        "saved_path": new_file_path,
        "image_url": image_url
    }