import models  # noqa: F401  (needed so SQLAlchemy knows the User and Ticket tables)
from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from models import User
from schemas import UserCreate, UserResponse
from security import hash_password
from sqlalchemy import select, text
from sqlalchemy.orm import Session

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


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
def register(user_data: UserCreate, db: Session = Depends(get_db)):
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
