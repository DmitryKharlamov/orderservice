from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CustomUser(Base):
    __tablename__ = 'accounts_customuser'

    id = Column(Integer, primary_key=True)
    phone = Column(String, unique=True)
    telegram_id = Column(String, nullable=True)

