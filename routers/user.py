from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from models.models import User
from middleware.jwt import verify_token

router = APIRouter()

# Get user route (now using dependency injection for token)
@router.get("/{user_id}")
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)  # Dependency injection for token data
):
    current_user_id = token_data["user_id"]
    is_seller = token_data["is_seller"]

    print(f"Current User ID: {current_user_id}, Is Seller: {is_seller}")

    # Fetch user from the database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    # Exclude password from response
    user_data = {key: value for key, value in user.__dict__.items() if key != 'password'}

    # If you want to add a seller-specific check, you can do it here
    if is_seller:
        print("Seller-specific logic can be added here!")

    return user_data


# Delete user route (now using dependency injection for token)
@router.delete("/{user_id}")
async def remove_user(
    user_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)  # Dependency injection for token data
):
    current_user_id = token_data["user_id"]
    is_seller = token_data["is_seller"]

    # Fetch user from the database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found!")

    # Check if the current user is trying to delete their own account
    if current_user_id != user.id:
        raise HTTPException(status_code=403, detail="You can delete only your own account!")

    # If seller-specific logic is needed, you can check it here
    if is_seller:
        print("Seller-specific delete logic can be added here!")

    # Delete user from the database
    db.delete(user)
    db.commit()

    return {"message": "User successfully deleted!"}
