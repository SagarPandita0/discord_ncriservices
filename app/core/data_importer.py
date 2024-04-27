import json

from sqlalchemy.exc import SQLAlchemyError

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
        with open(json_file_path, "r") as file:
            data = json.load(file)
        with SessionLocal() as db:
            for message_data in data["messages"]:
                author_id = message_data["author"]["id"]
                author = db.query(Author).filter_by(id=author_id).first()
                if not author:
                    author = Author(id=author_id, name=message_data["author"]["name"])
                    db.add(author)
                message = Message(
                    id=message_data["id"],
                    timestamp=message_data["timestamp"],
                    content=message_data["content"],
                    author_id=author_id,
                )
                db.add(message)
            db.commit()
    except json.JSONDecodeError as e:
        print("An error occurred while reading JSON: %s", e)
    except SQLAlchemyError as e:
        print("An error occurred in the database: %s", e)
