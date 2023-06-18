from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://postgres:delio@localhost:5432/item_db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
