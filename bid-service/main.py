from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bids = []
highest_bids = {}

class BidCreate(BaseModel):
    auction_id: str
    amount: float

class Bid(BaseModel):
    user_id: str
    auction_id: str
    amount: float

class BidOut(Bid):
    timestamp: datetime
    id: str

@app.post("/bids", response_model=BidOut)
def place_bid(b: BidCreate, x_user_email: str = Header(...)):
    # auction existence should be checked in a real app
    current = highest_bids.get(b.auction_id, 0)
    if b.amount <= current:
        raise HTTPException(status_code=400, detail="Bid must be higher than current highest")

    bid_id = str(uuid.uuid4())
    bid_entry = {
        "user_id": x_user_email,
        **b.dict(),
        "id": bid_id,
        "timestamp": datetime.utcnow()
    }
    bids.append(bid_entry)
    highest_bids[b.auction_id] = b.amount
    return bid_entry

@app.get("/highest/{auction_id}")
def get_highest_bid(auction_id: str):
    highest_amount = highest_bids.get(auction_id)
    if not highest_amount:
        raise HTTPException(status_code=404, detail="No bids found for this auction")

    # Find the bid entry that matches the highest amount
    winner_bid = None
    for bid in reversed(bids): # Search from the newest bids
        if bid["auction_id"] == auction_id and bid["amount"] == highest_amount:
            winner_bid = bid
            break
    
    if not winner_bid:
         raise HTTPException(status_code=404, detail="Could not determine the winner")

    return winner_bid

@app.get("/auction/{auction_id}", response_model=List[BidOut])
def get_bids_for_auction(auction_id: str):
    return [b for b in bids if b["auction_id"] == auction_id]

@app.get("/user/{user_id}", response_model=List[BidOut])
def get_bids_for_user(user_id: str):
    return [b for b in bids if b["user_id"] == user_id]

@app.get("/health")
def health_check():
    return {"status": "auction-service is up and running"}
