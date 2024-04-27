from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    id = Column(String, primary_key=True)
    name = Column(String)


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True)
    content = Column(Text)
    timestamp = Column(DateTime, index=True)
    author_id = Column(String, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="messages")


Author.messages = relationship("Message", order_by=Message.id, back_populates="author")
