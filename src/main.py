from fastapi import FastAPI
from .api.routes import router as product_router
from .api.auth import router as auth_router
from .database.connection import DatabaseConnection

app = FastAPI(title="Cereal API")

# Initialize database
db_connection = DatabaseConnection()
db_connection.init_db()
db_connection.init_users()

# Include routers
app.include_router(product_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Cereal API"}