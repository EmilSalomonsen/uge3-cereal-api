import csv
from ..database.connection import DatabaseConnection

def import_csv_to_mongodb(csv_file_path: str):
    db = DatabaseConnection().get_db()
    
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        products = []
        
        for row in csv_reader:
            # Konverter string værdier til korrekte datatyper
            product = {
                "name": row["name"],
                "mfr": row["mfr"],
                "type": row["type"],
                "calories": int(row["calories"]),
                "protein": float(row["protein"]),
                "fat": float(row["fat"]),
                "sodium": int(row["sodium"]),
                "fiber": float(row["fiber"]),
                "carbo": float(row["carbo"]),
                "sugars": float(row["sugars"]),
                "potass": int(row["potass"]),
                "vitamins": int(row["vitamins"]),
                "shelf": int(row["shelf"]),
                "weight": float(row["weight"]),
                "cups": float(row["cups"]),
                "rating": float(row["rating"])
            }
            products.append(product)
        
        if products:
            db.products.insert_many(products) 