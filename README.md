# CloudDesk AI

An IT service management portal where users submit and track support tickets. AI features (planned) will suggest each ticket's category and priority, helping IT staff save time.

## Status

**Work in progress: Week 1 complete**

Working so far:
- User registration
- Login with JWT authentication
- Submit IT support tickets
- View my tickets (each user sees only their own)
- Log out
- Simple web pages (register, login, tickets)

## Tech stack

| Area | Tools |
|---|---|
| **Backend** | Python, FastAPI, SQLAlchemy, Pydantic, Uvicorn |
| **Database** | PostgreSQL (running in Docker) |
| **Security** | bcrypt password hashing, JWT tokens (PyJWT), CORS |
| **Frontend** | HTML, CSS, JavaScript (fetch) |
| **Tools** | Docker, Git and GitHub, WSL (Ubuntu), VS Code, DBeaver, Ruff |

## Run it locally

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Python 3.11 or newer
- Git

### 1. Clone the repository
```bash
git clone https://github.com/Raghdah-AlGahdari/clouddesk-ai.git
cd clouddesk-ai
```

### 2. Create your environment file
Copy the example file and fill in your own values:
```bash
cp .env.example .env
```
Generate a secret key for `SECRET_KEY`:
```bash
openssl rand -hex 32
```

### 3. Start the database
```bash
docker compose up -d
```

### 4. Set up Python and start the API
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend
python -m uvicorn main:app --reload
```
The API runs at `http://localhost:8000`. Interactive API docs are at `http://localhost:8000/docs`.

### 5. Start the frontend
In a second terminal:
```bash
cd frontend
python3 -m http.server 5500
```
Open `http://localhost:5500/register.html` in your browser.

## Roadmap

- [x] **Week 1:** Backend API, database, authentication, tickets and simple web pages
- [ ] Page styling
- [ ] Ticket status updates and an IT agent role
- [ ] Run the whole app in Docker
- [ ] Deploy to AWS
- [ ] AI features: suggest ticket category and priority
