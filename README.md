# OAuth 2.0 vs Traditional Authentication: Credential Stuffing Defense Analysis

A MERN application used for research comparing OAuth 2.0 and password-based authentication security against credential stuffing attacks.

## Research Paper

**Author:** Harsh Kumar ([@Harsh13912](https://github.com/Harsh13912))  
**Contact:** researchwithharsh@gmail.com

**Citation:** Kumar, H. (2026). Eliminating Credential Stuffing Attack Surfaces: A Comparative Analysis of OAuth 2.0 and Password-Based Authentication.

---

## Repository Location

This project is located at:  
`https://github.com/harshk160/Research---Eliminating-Credential-Stuffing-Attack-Surfaces/oauth-login-project/`

```
oauth-login-project/
├── server/                    # Backend (Node.js + Express)
├── client/                    # Frontend (React)
├── attack-simulator/          # Python credential stuffing script
│   ├── credential_stuffer.py
│   ├── combolist.csv         # 101 test credentials
│   └── data/                 # Results output
└── README.md
```

---

## System Requirements

- Node.js 16+
- Python 3.8+
- MongoDB 4.4+
- 8GB RAM minimum

---

## Reproducibility Instructions

### 1. Clone Repository

```bash
git clone https://github.com/harshk160/Research---Eliminating-Credential-Stuffing-Attack-Surfaces.git
cd Research---Eliminating-Credential-Stuffing-Attack-Surfaces/oauth-login-project
```

### 2. Start MongoDB

```bash
mongod
```

### 3. Backend Setup

```bash
cd server
npm install
cp .env.example .env
# Edit .env: Set MONGO_URI, JWT_SECRET, SESSION_SECRET
npm start
```

Backend runs at `http://localhost:5000`

### 4. Frontend Setup (Optional)

```bash
cd client
npm install
echo "VITE_API_URL=http://localhost:5000/api" > .env
npm run dev
```

Frontend runs at `http://localhost:5173`

### 5. Run Attack Simulation

```bash
cd attack-simulator
pip install -r requirements.txt
python credential_stuffer.py
```

**Results saved to:**
- `data/attack_results.csv` - Per-request logs (202 requests)
- `data/attack_metrics.json` - Aggregated statistics

---

## Environment Variables

**Minimum required in `server/.env`:**

```env
MONGO_URI=mongodb://localhost:27017/oauth-research
JWT_SECRET=your_secret_here
SESSION_SECRET=your_session_secret_here
```

---

## Live Deployment

- **Frontend:** [https://oauthloginproject.netlify.app](https://oauthloginproject.netlify.app)
- **Backend:** [https://my-oauth-server.onrender.com/api/health](https://my-oauth-server.onrender.com/api/health)

---

## Data Files

- **combolist.csv:** 100 synthetic + 1 valid test credential
- **attack_results.csv:** Detailed per-request logs
- **attack_metrics.json:** Success rate, response times, error distribution

---

## Ethical Considerations

All experiments conducted on localhost with synthetic data. No real user credentials used.

---

## Troubleshooting

**Backend won't start:**
- Verify MongoDB is running
- Check `.env` configuration

**Attack script fails:**
- Ensure backend is running on port 5000
- Verify `combolist.csv` exists

**No results generated:**
- Check write permissions in `data/` directory

---

## License

MIT License - See LICENSE file for details.

---

**⭐ Star this repo if you found it helpful!**
