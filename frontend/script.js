// API endpoints
const API_BASE_URL = 'http://localhost:8000';
const AUTH_ENDPOINTS = {
    register: `${API_BASE_URL}/users/register`,
    login: `${API_BASE_URL}/users/login`
};
const AUCTION_ENDPOINTS = {
    create: `${API_BASE_URL}/auctions/auctions`,
    list: `${API_BASE_URL}/auctions/auctions`,
    get: (id) => `${API_BASE_URL}/auctions/auctions/${id}`,
    delete: (id) => `${API_BASE_URL}/auctions/auctions/${id}`
};
const BID_ENDPOINTS = {
    create: `${API_BASE_URL}/bids/bids`,
    getByAuction: (auctionId) => `${API_BASE_URL}/bids/auction/${auctionId}`,
    getByUser: (userId) => `${API_BASE_URL}/bids/user/${userId}`
};

// State management
let currentUser = null;
let authToken = localStorage.getItem('authToken');

// Helper functions
function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => section.classList.add('hidden'));
    document.getElementById(sectionId).classList.remove('hidden');
}

async function fetchWithAuth(url, options = {}) {
    if (!authToken) {
        throw new Error('No authentication token');
    }
    
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
        ...options.headers
    };

    const response = await fetch(url, {
        ...options,
        headers
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
}

// Authentication functions
async function register() {
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    try {
        const response = await fetch(AUTH_ENDPOINTS.register, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, password })
        });

        if (response.ok) {
            alert('Registration successful! Please login.');
        } else {
            throw new Error('Registration failed');
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch(AUTH_ENDPOINTS.login, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (response.ok) {
            authToken = data.access_token;
            localStorage.setItem('authToken', authToken);
            currentUser = { email };
            showSection('auction-section');
            loadAuctions();
        } else {
            throw new Error('Login failed');
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Auction functions
async function createAuction() {
    const title = document.getElementById('auction-title').value;
    const description = document.getElementById('auction-description').value;
    const starting_price = parseFloat(document.getElementById('auction-price').value);
    const ends_at = new Date(document.getElementById('auction-end-time').value).toISOString();

    try {
        await fetchWithAuth(AUCTION_ENDPOINTS.create, {
            method: 'POST',
            body: JSON.stringify({
                title,
                description,
                starting_price,
                ends_at
            })
        });

        alert('Auction created successfully!');
        loadAuctions();
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function loadAuctions() {
    try {
        const auctions = await fetchWithAuth(AUCTION_ENDPOINTS.list);
        const container = document.getElementById('auctions-container');
        container.innerHTML = '';

        auctions.forEach(auction => {
            const card = document.createElement('div');
            card.className = 'auction-card';
            
            const status = getAuctionStatus(auction.ends_at);
            const statusClass = `status-${status.toLowerCase()}`;

            card.innerHTML = `
                <h4>${auction.title}</h4>
                <p>${auction.description}</p>
                <p>Current Price: $${(auction.current_price || auction.starting_price).toFixed(2)}</p>
                <p>Ends at: ${new Date(auction.ends_at).toLocaleString()}</p>
                <span class="status-badge ${statusClass}">${status}</span>
                
                ${auction.winner ? `
                    <div class="winner-info">
                        <strong>Winner:</strong> ${auction.winner}
                    </div>
                ` : ''}

                <div class="auction-actions">
                    <button class="view-bids-btn" onclick="toggleBidHistory('${auction.id}')">View Bids</button>
                </div>

                ${status === 'LIVE' ? `
                    <div class="bid-form">
                        <input type="number" placeholder="Bid amount" id="bid-amount-${auction.id}" step="0.01">
                        <button onclick="placeBid('${auction.id}')">Place Bid</button>
                    </div>
                ` : ''}

                <div class="bid-history hidden" id="bid-history-${auction.id}">
                    <h5>Bid History:</h5>
                    <ul></ul>
                </div>
            `;
            
            container.appendChild(card);
        });
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

function getAuctionStatus(endsAt) {
    const now = new Date();
    const endDate = new Date(endsAt);
    
    if (endDate < now) {
        return 'ENDED';
    } else if (now < endDate) {
        return 'LIVE';
    } else {
        return 'PENDING';
    }
}

async function placeBid(auctionId) {
    const amount = parseFloat(document.getElementById(`bid-amount-${auctionId}`).value);

    try {
        await fetchWithAuth(BID_ENDPOINTS.create, {
            method: 'POST',
            body: JSON.stringify({
                auction_id: auctionId,
                amount
            })
        });

        alert('Bid placed successfully!');
        loadAuctions();
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function toggleBidHistory(auctionId) {
    const historyContainer = document.getElementById(`bid-history-${auctionId}`);
    const isHidden = historyContainer.classList.contains('hidden');

    if (!isHidden) {
        historyContainer.classList.add('hidden');
        historyContainer.querySelector('ul').innerHTML = ''; // Clear content when hiding
        return;
    }

    try {
        const bids = await fetchWithAuth(BID_ENDPOINTS.getByAuction(auctionId));
        const bidList = historyContainer.querySelector('ul');
        bidList.innerHTML = ''; // Clear previous content

        if (bids.length === 0) {
            bidList.innerHTML = '<li>No bids have been placed yet.</li>';
        } else {
            bids.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)); // Show newest first
            bids.forEach(bid => {
                const li = document.createElement('li');
                li.textContent = `Bidder: ${bid.user_id}, Amount: $${bid.amount.toFixed(2)} at ${new Date(bid.timestamp).toLocaleString()}`;
                bidList.appendChild(li);
            });
        }
        
        historyContainer.classList.remove('hidden');

    } catch (error) {
        alert(`Error loading bid history: ${error.message}`);
    }
}

function logout() {
    authToken = null;
    localStorage.removeItem('authToken');
    showSection('auth-section');
    // Clear auction list to prevent old data from showing on next login
    document.getElementById('auctions-container').innerHTML = '';
}

// Initialize the application
function init() {
    authToken = localStorage.getItem('authToken'); // Make sure we get the latest token from storage
    if (authToken) {
        showSection('auction-section');
        loadAuctions();
    } else {
        showSection('auth-section');
    }
}

// Start the application
init();
