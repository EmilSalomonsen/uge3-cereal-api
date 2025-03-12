from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..schemas.user import UserCreate, UserResponse, Token
from ..utils.security import verify_password, get_password_hash, create_access_token
from ..database.connection import DatabaseConnection
from datetime import timedelta
from bson import ObjectId
from jose import jwt, JWTError
from ..utils.security import SECRET_KEY, ALGORITHM

router = APIRouter()
db = DatabaseConnection().get_db()

# Setup OAuth2 med token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

@router.post("/auth/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    # Tjek om email allerede eksisterer
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Opret ny bruger med hashet password
    user_dict = user.model_dump()  # Bemærk: .dict() er forældet, brug .model_dump()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    
    # Gem i database
    result = db.users.insert_one(user_dict)
    created_user = db.users.find_one({"_id": result.inserted_id})
    
    return UserResponse.from_mongo(created_user)  

@router.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Find bruger
    user = db.users.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Verificer password
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Opret access token
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=timedelta(minutes=30)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user = db.users.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return UserResponse.from_mongo(user)