from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.database import get_db

app = FastAPI()
DB_DEPENDENCY = Depends(get_db)


@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}


@app.get("/health/db")
def health_check(db: Session = DB_DEPENDENCY):
    try:
        db.execute(text("SELECT 1"))
        return {"database": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="database unavailable")
