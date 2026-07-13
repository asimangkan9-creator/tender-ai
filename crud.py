from typing import List, Optional
from bson import ObjectId
from database import tenders_collection
from models import Tender, TenderCreate

async def create_tender(tender: TenderCreate) -> Tender:
    result = await tenders_collection.insert_one(tender.model_dump())
    created = await tenders_collection.find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return Tender(**created)

async def get_tender(tender_id: str) -> Optional[Tender]:
    tender = await tenders_collection.find_one({"_id": ObjectId(tender_id)})
    if tender:
        tender["_id"] = str(tender["_id"])
        return Tender(**tender)
    return None

async def get_all_tenders(limit: int = 100) -> List[Tender]:
    cursor = tenders_collection.find().limit(limit)
    tenders = []
    async for tender in cursor:
        tender["_id"] = str(tender["_id"])
        tenders.append(Tender(**tender))
    return tenders

async def search_tenders(keyword: str, location: Optional[str] = None) -> List[Tender]:
    query = {
        "$or": [
            {"title": {"$regex": keyword, "$options": "i"}},
            {"department": {"$regex": keyword, "$options": "i"}},
            {"summary": {"$regex": keyword, "$options": "i"}},
        ]
    }
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    cursor = tenders_collection.find(query)
    tenders = []
    async for tender in cursor:
        tender["_id"] = str(tender["_id"])
        tenders.append(Tender(**tender))
    return tenders

async def update_tender(tender_id: str, tender: TenderCreate) -> Optional[Tender]:
    result = await tenders_collection.update_one(
        {"_id": ObjectId(tender_id)},
        {"$set": tender.model_dump()}
    )
    if result.modified_count:
        updated = await tenders_collection.find_one({"_id": ObjectId(tender_id)})
        updated["_id"] = str(updated["_id"])
        return Tender(**updated)
    return None

async def delete_tender(tender_id: str) -> bool:
    result = await tenders_collection.delete_one({"_id": ObjectId(tender_id)})
    return result.deleted_count > 0