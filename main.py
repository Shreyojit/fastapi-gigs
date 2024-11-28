from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from routers import auth,user
from db import Base, engine


from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Initialize the FastAPI app
app = FastAPI()

# CORS settings
allowed_origins = [
    "http://localhost:3000",
    "https://freelance-space-1m7r4fbnu-shreyos-projects.vercel.app",
    "https://yourdomain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
Base.metadata.create_all(bind=engine)

# Root route
@app.get("/")
async def root():
    return {"message": "Backend is running!"}

# Include routers for authentication
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(user.router, prefix="/api/users", tags=["Users"])
