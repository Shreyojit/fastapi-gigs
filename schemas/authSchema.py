from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    is_seller: bool

class LoginRequest(BaseModel):
    username: str
    password: str
