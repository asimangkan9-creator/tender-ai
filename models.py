from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Tender(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    title: str
    department: str
    published_date: Optional[str] = None
    closing_date: Optional[str] = None
    opening_date: Optional[str] = None
    tender_value: Optional[str] = None
    reference_link: str
    summary: Optional[str] = None
    location: Optional[str] = None
    source: Optional[str] = "assam"
    category: Optional[str] = None
    state: Optional[str] = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class TenderCreate(BaseModel):
    title: str
    department: str
    published_date: Optional[str] = None
    closing_date: Optional[str] = None
    opening_date: Optional[str] = None
    tender_value: Optional[str] = None
    reference_link: str
    summary: Optional[str] = None
    location: Optional[str] = None
    source: Optional[str] = "assam"
    category: Optional[str] = None
    state: Optional[str] = None


class SearchRequest(BaseModel):
    keyword: str
    location: Optional[str] = None
    source: Optional[str] = None