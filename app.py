import json
from bson import ObjectId
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from database import init_db, close_db
from models import TenderCreate, SearchRequest
from crud import create_tender, get_tender, get_all_tenders, search_tenders, update_tender, delete_tender
from ai_service import get_ai_recommendation, chat_with_ai

def json_encoder(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(title="Tender Search AI", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Tender Search AI API"}

@app.post("/tenders")
async def add_tender(tender: TenderCreate):
    result = await create_tender(tender)
    return json.loads(json.dumps(result.model_dump(), default=json_encoder))

@app.get("/tenders")
async def list_tenders(limit: int = 100):
    tenders = await get_all_tenders(limit)
    return [json.loads(json.dumps(t.model_dump(), default=json_encoder)) for t in tenders]

@app.get("/tenders/{tender_id}")
async def get_tender_by_id(tender_id: str):
    tender = await get_tender(tender_id)
    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")
    return json.loads(json.dumps(tender.model_dump(), default=json_encoder))

@app.put("/tenders/{tender_id}")
async def update_tender_by_id(tender_id: str, tender: TenderCreate):
    updated = await update_tender(tender_id, tender)
    if not updated:
        raise HTTPException(status_code=404, detail="Tender not found")
    return json.loads(json.dumps(updated.model_dump(), default=json_encoder))

@app.delete("/tenders/{tender_id}")
async def delete_tender_by_id(tender_id: str):
    deleted = await delete_tender(tender_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tender not found")
    return {"message": "Tender deleted"}

@app.post("/search")
async def search(request: SearchRequest):
    try:
        tenders = await search_tenders(request.keyword, request.location)
        if not tenders:
            return {"ai_answer": "No tenders found.", "results": []}
        ai_answer = await get_ai_recommendation(request.keyword, [t.model_dump() for t in tenders])
        results = []
        for t in tenders:
            d = t.model_dump()
            d["id"] = str(d.get("id", ""))
            results.append(d)
        return {"ai_answer": ai_answer, "results": results}
    except Exception as e:
        return {"ai_answer": f"Error: {str(e)}", "results": []}