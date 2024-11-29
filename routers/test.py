from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from models.models import User
from middleware.jwt import verify_token

router = APIRouter()

# Example route that requires the user to be a seller
@router.get("/restricted")
async def restricted_area(
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)  # Inject both user_id and is_seller
):
    current_user_id = token_data["user_id"]
    is_seller = token_data["is_seller"]
    
    print(f"User ID: {current_user_id}, Is Seller: {is_seller}")
    
    # If the user is not a seller, raise an error
    if not is_seller:
        raise HTTPException(status_code=403, detail="Only sellers can access this area!")

    # Continue with the business logic for sellers
    # For example, retrieve seller-specific data
    seller_data = db.query(User).filter(User.id == current_user_id).first()
    if not seller_data:
        raise HTTPException(status_code=404, detail="Seller not found!")

    return {"message": "Welcome to the seller's area", "seller_info": seller_data}

