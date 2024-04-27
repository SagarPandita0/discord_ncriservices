import logging
import os
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import and_, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
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


@router.get("/search_by_date", response_model=List[SearchResult])
async def search_by_date(
    start_date: datetime = Query(...), end_date: datetime = Query(...)
) -> List[SearchResult]:
    """
    Endpoint to search messages by date range in the database.

    Args:
        start_date (datetime): The start date of the search range.
        end_date (datetime): The end date of the search range.

    Returns:
        List[SearchResult]: A list of search results within the specified date range.

    Raises:
        HTTPException: If there is a database error.
    """
    with SessionLocal() as db:
        logging.info(f"Received start_date: {start_date}, end_date: {end_date}")
        try:
            query = (
                db.query(Message, Author.name, Message.timestamp)
                .join(Author, Message.author_id == Author.id)
                .filter(
                    and_(Message.timestamp >= start_date, Message.timestamp <= end_date)
                )
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
            logging.error("Database error occurred: %s", e)
            raise HTTPException(status_code=500, detail=str(e))
