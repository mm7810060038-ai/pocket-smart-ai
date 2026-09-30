from typing import Optional
from pydantic import BaseModel, Field

class HomeRequest(BaseModel):
    budget: float = Field(gt=0)
    room: str = Field(min_length=1, max_length=100)
    style: str = Field(default="Modern", max_length=100)
    items: str = Field(default="Lights, fan, table", max_length=500)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0)
    guests: int = Field(gt=0, le=10000)
    event_type: str = Field(min_length=1, max_length=100)
    venue: str = Field(default="Chennai", max_length=200)

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0)
    occasion: str = Field(min_length=1, max_length=100)
    style: str = Field(default="Elegant", max_length=100)
    outfit: Optional[str] = Field(default=None, max_length=500)
