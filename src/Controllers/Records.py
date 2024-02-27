from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel, parse_obj_as
from fastapi.middleware.cors import CORSMiddleware
from src.Models.Collections import DocumentKey, User, Record, string_to_objectid
from typing import List, Optional
from pymongo import DESCENDING
from datetime import datetime

client = MongoClient("mongodb+srv://jony:1234@punchin.fou70xw.mongodb.net/")
db = client["PunchIn-Dev"]
collection = db["Records"]

class ClockOutUser(BaseModel):
    userId: str

router = APIRouter()

@router.put("/records/clock-in", response_model=Record, tags=["Records"])
async def insert_record(record: Record):
    print(record)
    record_dict = record.dict()
    if record_dict["clockOutTime"] is None:
        del record_dict["clockOutTime"]  # Rem
        

    del record_dict["id"]
   
    last_record = await get_last_record(record.user.id)
    if last_record.clockOutTime:
        record_dict["user"]["id"] = string_to_objectid(record_dict["user"]["id"])
        collection.insert_one(record_dict)
        res = collection.find_one(record_dict)
        return parse_obj_as(Record, res)
    raise HTTPException(status_code=400, detail="User already clocked in")

@router.post("/records/clock-out", response_model=Record, tags=["Records"])
async def clock_out(user: ClockOutUser):
    last_record = await get_last_record(user.userId)
    if last_record.clockOutTime:
        raise HTTPException(status_code=400, detail="User already clocked out")
    collection.update_one(
        {"_id": string_to_objectid(last_record.id)},
        {"$set": {"clockOutTime": datetime.now()}}
    )
    res = collection.find_one({"_id": string_to_objectid(last_record.id)})
    return parse_obj_as(Record, res)

@router.put("/records/first-record", response_model=Record, tags=["Records"], description="Insert a record for the first time")
async def insert_record(user: DocumentKey):
    record = {
        "user": {"id": string_to_objectid(user.id), "name": user.name},
        "clockInTime": datetime.now()
    }
    collection.insert_one(record)
    inserted_record = collection.find_one(record)
    return parse_obj_as(Record, inserted_record)

async def get_last_record(userId: str):
    record = collection.find_one(
        {"user.id": string_to_objectid(userId)},
        sort=[("clockInTime", DESCENDING)]
    )
    if record:
        return parse_obj_as(Record, record)
    raise HTTPException(status_code=404, detail="Record not found")

@router.get("/records/{userId}/get-latest-record", response_model=Record, tags=["Records"])
async def get_latest_record(userId: str):
    res = await get_last_record(userId)
    res.user.id = (userId)
    return res

@router.get("/records/{userId}", response_model=List[Record], tags=["Records"])
async def get_user_records(userId: str):
    records = list(collection.find({"user.id": string_to_objectid(userId)}).sort("clockInTime", DESCENDING).limit(5))
    return parse_obj_as(List[Record], records)