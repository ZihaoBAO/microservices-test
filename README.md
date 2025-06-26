# Real-Time Auction Platform (Microservices)

This project implements a real-time auction platform using a microservices architecture. It demonstrates the integration of multiple backend services with a frontend user interface to create a complete, interactive system.

## Project Overview

The platform allows users to register, log in, create auctions for items, view active auctions, and place bids in real-time. Once an auction's time expires, the system automatically determines the highest bidder and notifies them as the winner.

The entire system is built with a decoupled architecture, where each core business logic (users, auctions, bids) is handled by its own dedicated service.

## Architecture

The system consists of five main components:
- **User Service**: Handles user registration and login.
- **Auction Service**: Manages the creation and listing of auctions. It also contains the logic to determine winners when an auction ends.
- **Bid Service**: Manages the process of placing and retrieving bids for auctions.
- **Auth Gateway**: Acts as a single entry point for all incoming requests. It is responsible for request routing and JWT-based authentication, ensuring that only authorized requests reach the protected services.
- **Frontend**: A single-page application (SPA) built with vanilla HTML, CSS, and JavaScript that provides the user interface for interacting with the platform.

## Features Implemented
- **User Authentication**: Secure user registration and login using JWT.
- **Auction Management**: Users can create auctions with a title, description, starting price, and end time.
- **Real-Time Bidding**: Authenticated users can place bids on any live auction.
- **Dynamic Auction Status**: Auctions are automatically transitioned between `PENDING`, `LIVE`, and `ENDED` states.
- **Winner Notification**: Once an auction ends, the system automatically identifies the highest bidder and marks them as the winner (simulated via backend console logs and UI update).
- **Bid History**: Users can view the full bidding history for any auction.

## How to Run the Platform

To run the platform, you need to start all four backend services and the frontend server.

### 1. Start Backend Services
Open a separate terminal for each service, navigate to its directory, and run the corresponding command.

**User Service (Port 5000)**
```bash
cd user-service
uvicorn main:app --reload --port 5000
```

**Auction Service (Port 5001)**
```bash
cd auction-service
uvicorn main:app --reload --port 5001
```

**Bid Service (Port 5002)**
```bash
cd bid-service
uvicorn main:app --reload --port 5002
```

**Auth Gateway (Port 8000)**
```bash
cd auth-gateway
uvicorn main:app --reload --port 8000
```

### 2. Start Frontend
Open a fifth terminal for the frontend.

```bash
cd frontend
python -m http.server 8080
```
*Note: If you don't have Python installed, you can use any simple HTTP server, like the "Live Server" extension in VS Code.*

### 3. Access the Application
Once all services are running, open your web browser and navigate to:
[http://localhost:8080](http://localhost:8080)

You can now register a new user, log in, and start using the auction platform.
