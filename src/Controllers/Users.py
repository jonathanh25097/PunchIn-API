from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel, parse_obj_as
from fastapi.middleware.cors import CORSMiddleware
from src.Models.Collections import User
from typing import List, Optional

client = MongoClient("mongodb+srv://jony:1234@punchin.fou70xw.mongodb.net/")
db = client["PunchIn-Dev"]
collection = db["Users"]

router = APIRouter()

class login(BaseModel):
    username: str
    password: str

@router.put("/users/insert", response_model=User, tags=["Users"])
async def create_user(user: User):
    if collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    user_dict = user.dict()
    # In a real app, you should hash the password before saving it
    collection.insert_one(user_dict)
    return user

@router.post("/users/login", response_model=User, tags=["Users"])
async def login_user(login : login):
    user = collection.find_one({"username": login.username, "password": login.password})
    if user:
        return User(**user)
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/users", response_model=List[User], tags=["Users"])
async def list_users():
    users = list(collection.find())
    
    return parse_obj_as(List[User], users)

@router.get("/users/{username}", response_model=User, tags=["Users"])
async def get_user(username: str):
    user = collection.find_one({"username": username})
    if user:
        return User(**user)
    raise HTTPException(status_code=404, detail="User not found")

