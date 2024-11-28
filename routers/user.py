from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from db import get_db
from models.models import User
from middleware.jwt import verify_token

router = APIRouter()

# Get user route
@router.get("/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db), request: Request = None):
    # Use the request object directly
    current_user_id = await verify_token(request)  # Get the user ID from the token
    
    # Fetch user from the database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    # Exclude password from response
    user_data = {key: value for key, value in user.__dict__.items() if key != 'password'}

    return user_data

# Delete user route
@router.delete("/{user_id}")
async def remove_user(user_id: int, db: Session = Depends(get_db), request: Request = None):
    current_user_id = await verify_token(request)  # Get the user ID from the token
    
    # Fetch user from the database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    # Check if the current user is trying to delete their own account
    if current_user_id != user.id:
        raise HTTPException(status_code=403, detail="You can delete only your own account!")

    # Delete user from the database
    db.delete(user)
    db.commit()

    return {"message": "User successfully deleted!"}
