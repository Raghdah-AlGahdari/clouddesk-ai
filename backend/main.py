import jwt
import models  # noqa: F401  (needed so SQLAlchemy knows the User and Ticket tables)
from config import settings
from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models import Ticket, User
from schemas import (
    LoginRequest,
    TicketCreate,
    TicketResponse,
    Token,
    UserCreate,
    UserResponse,
)
from security import create_access_token, hash_password, verify_password
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CloudDesk AI API", version="0.1.0")
bearer_scheme = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
) -> User:
    # 1. Take the token out of the "Authorization: Bearer <token>" header
    token = credentials.credentials

    # 2. Check the stamp (signature) and expiry, then read the user id
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = int(payload.get("sub"))
    except (jwt.InvalidTokenError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # 3. Find the user in the database
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # 4. Give the user to the endpoint that asked for it
    return user


@app.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):  # noqa: B008
    return current_user


@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}


@app.get("/health/db")
def health_check(db: Session = Depends(get_db)):  # noqa: B008
    try:
        db.execute(text("SELECT 1"))
        return {"database": "ok"}
    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=503, detail="database unavailable")


@app.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):  # noqa: B008
    # make the email lowercase
    email = user_data.email.lower()
    # check if the email already exists
    existing_user = (
        db.execute(select(User).where(User.email == email)).scalars().first()
    )
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    # hash the password
    hashed = hash_password(user_data.password)
    new_user = User(full_name=user_data.full_name, email=email, password_hash=hashed)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):  # noqa: B008
    email = login_data.email.lower()
    user = db.execute(select(User).where(User.email == email)).scalars().first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token(user.id)
    return Token(access_token=token)


@app.post("/tickets", response_model=TicketResponse, status_code=201)
def create_ticket(
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):  # noqa: B008
    new_ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        priority=ticket_data.priority,
        user_id=current_user.id,
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket


@app.get("/tickets", response_model=list[TicketResponse])
def list_my_tickets(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):  # noqa: B008
    tickets = (
        db.execute(select(Ticket).where(Ticket.user_id == current_user.id))
        .scalars()
        .all()
    )
    return tickets
