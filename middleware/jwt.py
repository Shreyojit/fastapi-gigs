from fastapi import Request, HTTPException, Depends
from jose import JWTError, jwt
import os

# JWT secret key and algorithm
SECRET_KEY = os.getenv("JWT_TOKEN")
ALGORITHM = "HS256"

# JWT verification middleware
async def verify_token(request: Request):
    token = request.cookies.get("accessToken")  # Get token from cookies
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized access!")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user_id = payload.get("id")  # Attach user ID to the request state
        request.state.is_seller = payload.get("isSeller")  # Optionally attach isSeller info
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token!")
