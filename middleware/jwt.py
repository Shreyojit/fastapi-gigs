from fastapi import Request, HTTPException, Depends
from jose import JWTError, jwt
import os

# JWT secret key and algorithm
SECRET_KEY = os.getenv("JWT_TOKEN")
ALGORITHM = "HS256"

# async def verify_token(request: Request):
#     cookies = request.cookies  # Get all cookies
#     print("Request Cookies:", cookies)  # Log the cookies to check if accessToken exists
#     token = cookies.get("accessToken")
#     if not token:
#         raise HTTPException(status_code=401, detail="Unauthorized access!")

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         request.state.user_id = payload.get("id")  # Attach user ID to the request state
#         request.state.is_seller = payload.get("isSeller")
#         return payload.get("id")  # Return user ID directly
#     except JWTError:
#         raise HTTPException(status_code=403, detail="Invalid token!")



# Updated verify_token function in middleware/jwt.py

async def verify_token(request: Request) -> dict:
    cookies = request.cookies  # Get all cookies
    print("Request Cookies:", cookies)  # Log the cookies to check if accessToken exists
    token = cookies.get("accessToken")
    
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized access!")

    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")  # Extract the user ID from the token payload
        is_seller = payload.get("isSeller")  # Extract the isSeller flag

        if not user_id:
            raise HTTPException(status_code=403, detail="Invalid token!")

        # Attach the user_id and is_seller to the request state (optional)
        request.state.user_id = user_id
        request.state.is_seller = is_seller
        
        return {"user_id": user_id, "is_seller": is_seller}  # Return both user_id and is_seller
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token!")
