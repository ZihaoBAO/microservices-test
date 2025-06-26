from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError
import httpx

app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost:8080",  # Allow your frontend to access
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

# Service address mapping (can be adjusted based on the path)
SERVICE_MAP = {
    "auctions": "http://localhost:5001",
    "bids": "http://localhost:5002",
    "users": "http://localhost:5000",
}

def verify_token(authorization: str):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid auth header")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


# New route for public access (no token required)
@app.api_route("/users/{path:path}", methods=["POST"])
async def public_gateway(path: str, request: Request):
    if path not in ["register", "login"]:
        raise HTTPException(status_code=403, detail="Permission denied for this endpoint")

    target_url = f"{SERVICE_MAP['users']}/{path}"
    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=target_url,
            headers={key.decode(): value.decode() for key, value in request.headers.raw if key.decode().lower() != "host"},
            content=await request.body()
        )
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=dict(resp.headers)
        )


@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service: str, path: str, request: Request, authorization: str = Header(...)):
    # 1. validate JWT
    payload = verify_token(authorization)
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(status_code=403, detail="User identifier not found in token")

    # 2. Determine whether to support this service
    if service not in SERVICE_MAP:
        raise HTTPException(status_code=404, detail="Service not found")

    # 3. Forward request
    target_url = f"{SERVICE_MAP[service]}/{path}"
    
    # Add user email to headers before forwarding
    forward_headers = {key.decode(): value.decode() for key, value in request.headers.raw if key.decode().lower() not in ["host", "authorization"]}
    forward_headers["X-User-Email"] = user_email

    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=target_url,
            headers=forward_headers,
            content=await request.body()
        )
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=dict(resp.headers)
        )


@app.get("/validate")
def validate_token_route(authorization: str = Header(...)):
    payload = verify_token(authorization)
    return {"user": payload["sub"]}


@app.get("/health")
def health_check():
    return {"status": "auth-gateway is running"}
