import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "tender_ai")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]
tenders_collection = db["tenders"]

async def init_db():
    await tenders_collection.create_indexes([
        IndexModel([("title", ASCENDING)]),
        IndexModel([("department", ASCENDING)]),
        IndexModel([("closing_date", ASCENDING)]),
        IndexModel([("reference_link", ASCENDING)], unique=True),
    ])

async def close_db():
    client.close()