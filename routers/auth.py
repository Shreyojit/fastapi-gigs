# routers/auth.py
from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from db import get_db  # Import the get_db function
from models.models import User
from schemas.authSchema import RegisterRequest, LoginRequest  # Import Pydantic models
import os

# Define password context and JWT settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_TOKEN")
ALGORITHM = "HS256"

router = APIRouter()

@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):  # Accept request as JSON
    hashed_password = pwd_context.hash(request.password)
    user = User(username=request.username, email=request.email, password=hashed_password, is_seller=request.is_seller)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User has been created.", "user": user}

@router.post("/login")
async def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):  # Accept request as JSON
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials!")
    
    token_data = {"id": user.id, "isSeller": user.is_seller}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    response.set_cookie(key="accessToken", value=token, httponly=False)
    return {"message": "Login successful", "user": {"id": user.id, "username": user.username, "isSeller": user.is_seller}}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("accessToken")
    return {"message": "User has been logged out."}
