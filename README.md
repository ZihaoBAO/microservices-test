# 🧱 Microservices Auction Platform

This project is a microservices-based auction platform built with FastAPI. It includes the following components:

- ✅ **User Service** — User registration and authentication
- 📦 **Auction Service** — Create and manage auctions
- 💰 **Bid Service** — Place and track bids
- 🛡️ **Auth Gateway** — Validate JWT tokens and route requests securely

---

## 🔧 Technologies Used

- FastAPI
- Python 3.11
- Uvicorn
- JWT (with `python-jose`)
- HTTP communication between services (no Docker used)

---

## 🧩 Microservice Architecture

                ┌────────────────────┐
                │   Auth Gateway     │
                │   (port 8000)      │
                └────────┬───────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐ ┌─────▼────────┐┌─────▼────────┐
│ User Service   │ │ Auction Svc │ │ Bid Service  │
│ (port 5000)    │ │ (port 5001) │ │ (port 5002)  │
└────────────────┘ └─────────────┘ └──────────────┘



## 🚀 How to Run

Open **four terminals** (or VSCode terminals) and start each service:

```bash
# 1. User Service
cd user-service
uvicorn main:app --reload --port 5000

# 2. Auction Service
cd auction-service
uvicorn main:app --reload --port 5001

# 3. Bid Service
cd bid-service
uvicorn main:app --reload --port 5002

# 4. Auth Gateway
cd auth-gateway
uvicorn main:app --reload --port 8000

## 🔐 JWT Token Generation

Use the helper script to generate a token:

```bash
cd auth-gateway
python generate_token.py

Copy the token and include it in your requests:
Authorization: Bearer <your_token>
