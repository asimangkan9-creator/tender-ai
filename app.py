from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import init_db, close_db
from models import TenderCreate, SearchRequest
from crud import (
    create_tender, get_tender, get_all_tenders,
    search_tenders, update_tender, delete_tender
)
from ai_service import get_ai_recommendation, chat_with_ai


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="Tender Search AI",
    description="AI-powered tender search and recommendation system",
    version="1.0.0",
    lifespan=lifespan
)

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
    existing = await get_tender_by_reference(tender.reference_link)
    if existing:
        raise HTTPException(status_code=400, detail="Tender already exists")
    return await create_tender(tender)


@app.get("/tenders")
async def list_tenders(limit: int = 100):
    return await get_all_tenders(limit)


@app.get("/tenders/{tender_id}")
async def get_tender_by_id(tender_id: str):
    tender = await get_tender(tender_id)
    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")
    return tender


@app.put("/tenders/{tender_id}")
async def update_tender_by_id(tender_id: str, tender: TenderCreate):
    updated = await update_tender(tender_id, tender)
    if not updated:
        raise HTTPException(status_code=404, detail="Tender not found")
    return updated


@app.delete("/tenders/{tender_id}")
async def delete_tender_by_id(tender_id: str):
    deleted = await delete_tender(tender_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tender not found")
    return {"message": "Tender deleted"}


@app.post("/search")
async def search(request: SearchRequest):
    tenders = await search_tenders(request.keyword, request.location)
    if not tenders:
        return {"ai_answer": "No tenders found matching your criteria.", "results": []}

    ai_answer = await get_ai_recommendation(request.keyword, [t.model_dump() for t in tenders])
    return {
        "ai_answer": ai_answer,
        "results": [t.model_dump() for t in tenders]
    }


@app.post("/chat")
async def chat(message: str):
    response = await chat_with_ai(message)
    return {"response": response}


async def get_tender_by_reference(reference_link: str):
    from database import tenders_collection
    tender = await tenders_collection.find_one({"reference_link": reference_link})
    return tender
