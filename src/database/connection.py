from pymongo import MongoClient
from dotenv import load_dotenv
import os
import csv
from pathlib import Path

load_dotenv()

class DatabaseConnection:
    _instance = None  # Singleton pattern - kun én database forbindelse

    def __new__(cls):
        """Singleton pattern - sikrer at vi kun har én database forbindelse"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
            print(f"Connecting to MongoDB at: {mongo_url}")
            cls._instance.client = MongoClient(mongo_url)
            cls._instance.db = cls._instance.client.cereal_db
        return cls._instance

    def get_db(self):
        """Returnerer database instansen"""
        return self.db

    def init_users(self):
        """Initialiserer users collection med unik email index"""
        try:
            self.db.users.create_index("email", unique=True)
            print("Users collection initialized")
        except Exception as e:
            print(f"Error initializing users collection: {e}")

    def init_db(self):
        """
        Initialiserer databasen med cerealdata fra CSV fil
        Konverterer datatyper og håndterer specielle formateringer
        """
        try:
            count = self.db.products.count_documents({})
            print(f"Current number of products in database: {count}")
            
            if count == 0:
                csv_path = Path(__file__).parent.parent.parent / 'data' / 'cereal.csv'
                print(f"Loading data from: {csv_path}")
                
                if not csv_path.exists():
                    print(f"Error: CSV file not found at {csv_path}")
                    return

                with open(csv_path, 'r') as file:
                    headers = file.readline().strip().split(';')
                    data_types = file.readline()  # Skip data types line
                    print(f"Found headers: {headers}")
                    
                    cereals = []
                    reader = csv.DictReader(file, fieldnames=headers, delimiter=';')
                    
                    for row in reader:
                        cereal = {}
                        for key, value in row.items():
                            key = key.strip()
                            value = value.strip() if value else "0"
                            
                            try:
                                if key in ['calories', 'protein', 'fat', 'sodium', 
                                         'potass', 'vitamins', 'shelf']:
                                    cereal[key] = int(float(value))
                                elif key in ['fiber', 'carbo', 'sugars', 'weight', 
                                          'cups']:
                                    cereal[key] = float(value)
                                elif key == 'rating':
                                    # Fjern tusindtalsseparator og konverter til float
                                    rating_value = value.replace('.', '')
                                    cereal[key] = float(rating_value) / 1000000  # Del med 1000000 for at få korrekt decimal
                                else:
                                    cereal[key] = value
                            except ValueError as e:
                                print(f"Error converting {key}: {value} - {e}")
                                if key in ['calories', 'protein', 'fat', 'sodium', 
                                         'potass', 'vitamins', 'shelf']:
                                    cereal[key] = 0
                                elif key in ['fiber', 'carbo', 'sugars', 'weight', 
                                          'cups', 'rating']:
                                    cereal[key] = 0.0
                                else:
                                    cereal[key] = value
                        
                        cereals.append(cereal)
                    
                    if cereals:
                        print(f"Inserting {len(cereals)} products into database")
                        self.db.products.insert_many(cereals)
                        print("Database initialized successfully")
                    else:
                        print("No data found in CSV file")
                        
        except Exception as e:
            print(f"Error initializing database: {e}")