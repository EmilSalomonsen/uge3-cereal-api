from fastapi import FastAPI
from .api.routes import router as product_router
from .database.connection import DatabaseConnection

app = FastAPI(title="Cereal API")

# Initialize database
db_connection = DatabaseConnection()
db_connection.init_db()

# Include routers
app.include_router(product_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Cereal API"}