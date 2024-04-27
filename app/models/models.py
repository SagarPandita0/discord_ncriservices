from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id = Column(BigInteger, primary_key=True)
    timestamp = Column(DateTime)
    content = Column(String)
    author_id = Column(BigInteger)

class Author(Base):
    __tablename__ = 'authors'
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
