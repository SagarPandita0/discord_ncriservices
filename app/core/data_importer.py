import json
import logging
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.models import Author, Message


def load_json_to_db(json_file_path: str):
    """
    Load JSON data containing Discord chat messages into the database.

    Args:
        json_file_path (str): The path to the JSON file containing chat messages.

    Raises:
        json.JSONDecodeError: If there is an error while reading JSON data.
        SQLAlchemyError: If there is an error in the database during the loading process.
    """
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        db: Session
        with SessionLocal() as db:
            # Cache to track authors already handled in this session to avoid redundant DB hits
            author_cache = {}
            for message_data in data["messages"]:
                author_data = message_data["author"]
                author_id = author_data["id"]
                if author_id not in author_cache:
                    # Check if the author already exists and get it, or create a new one
                    author = db.query(Author).get(author_id)
                    if not author:
                        author = Author(id=author_id, name=author_data.get("name"))
                        db.add(author)
                    author_cache[author_id] = author  # Cache it
                else:
                    author = author_cache[author_id]

                if not db.query(Message.id).filter_by(id=message_data["id"]).scalar():
                    message = Message(
                        id=message_data["id"],
                        timestamp=message_data["timestamp"],
                        content=message_data["content"],
                        author=author,
                    )
                    db.add(message)
                else:
                    logging.info(
                        "Skipping duplicate message with ID %s", message_data["id"]
                    )

            db.commit()
    except json.JSONDecodeError as e:
        logging.error("JSON decoding error: %s", e)
        raise
    except IntegrityError as e:
        logging.error("Database integrity error: %s", e)
        db.rollback()
        raise
    except SQLAlchemyError as e:
        logging.error("Database error: %s", e)
        db.rollback()
        raise
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
        db.rollback()
        raise
