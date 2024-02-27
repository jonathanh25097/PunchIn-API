from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from src.Controllers.Users import router as UsersRouter
from src.Controllers.Records import router as RecordsRouter

# Pydantic models for request and response data
class User(BaseModel):
    name: str
    email: str
    username: str
    password: str  # In a real app, passwords should be hashed
    phone_number: Optional[str] = None

# Initialize FastAPI app
app = FastAPI()

origins = [
    "*",
]

# Add CORSMiddleware to the application instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins (use ["*"] for all origins)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    allow_origin_regex=".*",
)

@app.get("/")
async def root():
    return {"message": "Welcome to Punch In App"}

app.include_router(UsersRouter)

app.include_router(RecordsRouter)