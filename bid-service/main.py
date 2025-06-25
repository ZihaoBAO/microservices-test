from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

app = FastAPI()

bids = []
highest_bids = {}

class Bid(BaseModel):
    user_id: str
    auction_id: str
    amount: float

class BidOut(Bid):
    timestamp: datetime
    id: str

@app.post("/bids", response_model=BidOut)
def place_bid(b: Bid):
    current = highest_bids.get(b.auction_id, 0)
    if b.amount <= current:
        raise HTTPException(status_code=400, detail="Bid must be higher than current highest")

    bid_id = str(uuid.uuid4())
    bid_entry = {
        **b.dict(),
        "id": bid_id,
        "timestamp": datetime.utcnow()
    }
    bids.append(bid_entry)
    highest_bids[b.auction_id] = b.amount
    return bid_entry

@app.get("/bids/auction/{auction_id}", response_model=List[BidOut])
def get_bids_for_auction(auction_id: str):
    return [b for b in bids if b["auction_id"] == auction_id]

@app.get("/bids/user/{user_id}", response_model=List[BidOut])
def get_bids_for_user(user_id: str):
    return [b for b in bids if b["user_id"] == user_id]

@app.get("/health")
def health_check():
    return {"status": "auction-service is up and running"}
