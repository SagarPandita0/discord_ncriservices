import os
from datetime import datetime
from typing import List
import logging

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


class AuthorSearchResult(BaseModel):
    author_name: str
    content: str
    timestamp: datetime


@router.get("/search_by_author", response_model=List[AuthorSearchResult])
async def search_by_author_name(
    author_name: str = Query(..., min_length=1, max_length=100)
) -> List[AuthorSearchResult]:
    """
    Endpoint to search messages by author name in the database.

    Args:
        author_name (str): The author's name to search for in message content.

    Returns:
        List[AuthorSearchResult]: A list of search results matching the author name.
    """
    with SessionLocal() as db:
        try:
            query = (
                db.query(Message.content, Author.name, Message.timestamp)
                .join(Author, Message.author_id == Author.id)
                .filter(Author.name.ilike(f"%{author_name}%"))
            )
            result = query.all()
            formatted_result = [
                AuthorSearchResult(
                    author_name=author_name,
                    content=message_content,
                    timestamp=message_timestamp,
                )
                for message_content, author_name, message_timestamp in result
            ]
            return formatted_result
        except SQLAlchemyError as e:
            logging.error("Database error occurred: %s", str(e))
            raise HTTPException(status_code=500, detail=f"Database error occurred: {e}")
