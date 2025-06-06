from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CustomUser(Base):
    __tablename__ = 'accounts_customuser'  # Точная таблица из Django!

    id = Column(Integer, primary_key=True)
    phone = Column(String, unique=True)
    telegram_id = Column(String, nullable=True)

# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import declarative_base, sessionmaker
#
# Base = declarative_base()
#
# class CustomUser(Base):
#     __tablename__ = 'accounts_customuser'
#     id = Column(Integer, primary_key=True)
#     phone = Column(String, unique=True)
#     telegram_id = Column(String)
#
# def get_session():
#     engine = create_engine("postgresql://postgres:postgres@db:5432/postgres")
#     Session = sessionmaker(bind=engine)
#     return Session()
