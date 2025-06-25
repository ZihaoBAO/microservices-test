from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import Response
from jose import jwt, JWTError
import httpx

app = FastAPI()

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


@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service: str, path: str, request: Request, authorization: str = Header(...)):
    # 1. validate JWT
    payload = verify_token(authorization)

    # 2. Determine whether to support this service
    if service not in SERVICE_MAP:
        raise HTTPException(status_code=404, detail="Service not found")

    # 3. Forward request
    target_url = f"{SERVICE_MAP[service]}/{path}"
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


@app.get("/validate")
def validate_token_route(authorization: str = Header(...)):
    payload = verify_token(authorization)
    return {"user": payload["sub"]}


@app.get("/health")
def health_check():
    return {"status": "auth-gateway is running"}
