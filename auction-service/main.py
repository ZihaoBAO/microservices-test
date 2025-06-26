from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone
import uuid
import httpx

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

auctions = {}
BID_SERVICE_URL = "http://localhost:5002"

class AuctionCreate(BaseModel):
    title: str
    description: str
    starting_price: float
    ends_at: datetime

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
    winner: Optional[str] = None

@app.post("/auctions", response_model=AuctionOut)
def create_auction(a: AuctionCreate, x_user_email: str = Header(...)):
    auction_id = str(uuid.uuid4())
    auctions[auction_id] = {
        **a.dict(),
        "id": auction_id,
        "owner_id": x_user_email,
        "current_price": a.starting_price,
        "status": "pending",
        "winner": None
    }
    return auctions[auction_id]

@app.get("/auctions", response_model=List[AuctionOut])
async def list_auctions():
    now = datetime.now(timezone.utc)
    for auction_id, auction in list(auctions.items()):
        # Check if auction has ended and status is not yet updated
        if auction["ends_at"] < now and auction["status"] != "ended":
            try:
                # Call bid service to get the winner
                async with httpx.AsyncClient() as client:
                    resp = await client.get(f"{BID_SERVICE_URL}/highest/{auction_id}")
                
                if resp.status_code == 200:
                    winner_data = resp.json()
                    winner_email = winner_data["user_id"]
                    auction["winner"] = winner_email
                    auction["current_price"] = winner_data["amount"] # Final price
                    print(f"🎉 Notifying winner {winner_email} for auction '{auction['title']}'! 🎉")
                else:
                    # No bids were placed
                    print(f"ℹ️ Auction '{auction['title']}' ended with no bids.")

            except httpx.RequestError as e:
                print(f"Error calling bid service: {e}")
            finally:
                # Update status regardless of winner
                auction["status"] = "ended"

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