from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

app = FastAPI()

auctions = {}

class Auction(BaseModel):
    title: str
    description: str
    starting_price: float
    ends_at: datetime
    owner_id: str

class AuctionOut(Auction):
    id: str
    current_price: float
    status: str  # pending / live / ended

@app.post("/auctions")
def create_auction(a: Auction):
    auction_id = str(uuid.uuid4())
    auctions[auction_id] = {
        **a.dict(),
        "id": auction_id,
        "current_price": a.starting_price,
        "status": "pending"
    }
    return auctions[auction_id]

@app.get("/auctions", response_model=List[AuctionOut])
def list_auctions():
    return list(auctions.values())

@app.get("/auctions/{auction_id}", response_model=AuctionOut)
def get_auction(auction_id: str):
    if auction_id not in auctions:
        raise HTTPException(status_code=404, detail="Auction not found")
    return auctions[auction_id]

@app.delete("/auctions/{auction_id}")
def delete_auction(auction_id: str):
    if auction_id not in auctions:
        raise HTTPException(status_code=404, detail="Auction not found")
    del auctions[auction_id]
    return {"message": "Auction deleted"}

@app.get("/health")
def health_check():
    return {"status": "auction-service is up and running"}