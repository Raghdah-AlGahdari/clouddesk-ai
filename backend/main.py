import models  # noqa: F401  (needed so SQLAlchemy knows the User and Ticket tables)
from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
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
