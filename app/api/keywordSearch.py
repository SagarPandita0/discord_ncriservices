from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import logging
from app.models.models import Message,Author

load_dotenv()
router = APIRouter()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class SearchTerm(BaseModel):
    term: str

@router.get("/search")
async def search_by_keyword(search_term: str):
    db = SessionLocal()
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Received searchTERM: {search_term}")
    try:
        engine.connect()
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database connection failed.")
    try:
        query = db.query(Message,Author.name,Message.timestamp).join(Author,Message.author_id==Author.id).filter(Message.content.ilike(f"%{search_term}%"))
        logging.info(f"Received QUERY: {query}")
        result = query.all()
        formatted_result = [
            {"author_name": author_name,"content": message.content,"timestamp":timestamp}
            for message, author_name,timestamp in result
        ]
        return formatted_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
