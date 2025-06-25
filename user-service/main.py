from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
import httpx

app = FastAPI()
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

fake_users_db = {}

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/register")
def register(user: UserRegister):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    fake_users_db[user.email] = {
        "name": user.name,
        "email": user.email,
        "password": user.password 
    }
    return {"msg": "Registered successfully"}

@app.post("/login")
def login(user: UserLogin):
    db_user = fake_users_db.get(user.email)
    if not db_user or db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = jwt.encode(
        {"sub": user.email, "exp": datetime.utcnow() + timedelta(hours=2)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": token}

@app.get("/users")
def get_users():
    return fake_users_db

@app.get("/health")
def health_check():
    return {"status": "user-service is up and running"}

@app.get("/check-auction-service")
async def check_auction_service():
    auction_service_url = "http://127.0.0.1:5001/health"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(auction_service_url)
            response.raise_for_status()
            return {"auction_service_status": response.json()}
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error connecting to auction service: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=response.status_code, detail=f"Auction service error: {e.response.text}")

