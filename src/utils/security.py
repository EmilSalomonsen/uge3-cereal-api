from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Konfigurer password hashing med bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT konfiguration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY ikke sat i .env filen")
    
ALGORITHM = "HS256"  # Standard algoritme til JWT tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token udløber efter 30 minutter

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificerer at et password matcher det hashede password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genererer et sikkert hash af et password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Opretter et JWT token med brugerdata og udløbstid
    Hvis expires_delta ikke er angivet, udløber token efter 15 minutter
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt