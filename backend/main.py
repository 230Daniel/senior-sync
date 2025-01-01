
import os
from typing import List, Optional
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
import pymongo

load_dotenv()

mongo = pymongo.MongoClient(os.environ["MONGO_HOST"])
db = mongo.seniorsync
test_collection = db.test_collection

class Item(BaseModel):
    field1: Optional[str] = None
    field2: Optional[str] = None
    field3: Optional[str] = None

APP = FastAPI()

@APP.get("/")
async def read_root():
    items = test_collection.count_documents({})
    return f"hello, I am the backend, I speak for the trees. There are {items} items."

@APP.get("/items")
async def get_items() -> List[Item]:
    return list(test_collection.find({}))

@APP.post("/items")
async def post_items(item: Item):
    test_collection.insert_one(item.model_dump())
    return item
