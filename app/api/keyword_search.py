from datetime import datetime
import logging
import os
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.models.models import Author, Message

load_dotenv()
router = APIRouter()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not set")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class SearchResult(BaseModel):
    author_name: str
    content: str
    timestamp: datetime


@router.get("/search", response_model=List[SearchResult])
async def search_by_keyword(
    search_term: str = Query(..., min_length=1, max_length=100)
) -> List[SearchResult]:
    """
    Endpoint to search messages by keyword in the database.

    Args:
        search_term (str): The keyword to search for in message content.

    Returns:
        List[SearchResult]: A list of search results matching the keyword.

    Raises:
        HTTPException: If there is a database error.
    """
    with SessionLocal() as db:
        logging.info("Received searchTERM: %s", search_term)
        try:
            query = (
                db.query(Message, Author.name, Message.timestamp)
                .join(Author, Message.author_id == Author.id)
                .filter(Message.content.ilike(f"%{search_term}%"))
            )
            result = query.all()
            formatted_result = [
                SearchResult(
                    author_name=author_name,
                    content=message.content,
                    timestamp=timestamp,
                )
                for message, author_name, timestamp in result
            ]
            return formatted_result
        except SQLAlchemyError as e:
            logging.error("Database error occurred: %s", str(e))
            raise HTTPException(status_code=500, detail="Database error")
