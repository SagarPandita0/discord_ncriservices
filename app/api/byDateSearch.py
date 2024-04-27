from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from datetime import datetime
from app.models.models import Author, Message
import os
from dotenv import load_dotenv
import logging

load_dotenv()
router = APIRouter()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime

@router.get("/search_by_date")
async def search_by_date(start_date: datetime = Query(...), end_date: datetime = Query(...)):
    db = SessionLocal()
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Received start_date: {start_date}, end_date: {end_date}")
    try:
        engine.connect()
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database connection failed.")
    try:
        query = (db.query(Message, Author.name, Message.timestamp).join(Author, Message.author_id == Author.id).filter(and_(Message.timestamp >= start_date, Message.timestamp <= end_date)))
        result = query.all()
        formatted_result = [
            {"author_name": author_name, "content": message.content, "timestamp": timestamp}
            for message, author_name, timestamp in result
        ]
        return formatted_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
