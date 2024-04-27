import json
from app.database.database import SessionLocal
from app.models.models import Message, Author

def load_json_to_db(json_file_path: str):
    db = SessionLocal()
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        for message_data in data['messages']:
            author_id = message_data['author']['id']
            author = db.query(Author).filter_by(id=author_id).first()
            if not author:
                author = Author(id=author_id, name=message_data['author']['name'])
                db.add(author)
            message = Message(id=message_data['id'], timestamp=message_data['timestamp'],
                              content=message_data['content'], author_id=author_id)
            db.add(message)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()
