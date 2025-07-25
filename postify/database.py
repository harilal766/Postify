from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from postify.environment_variables import db_connection

Base = declarative_base()

engine = create_engine(db_connection)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
