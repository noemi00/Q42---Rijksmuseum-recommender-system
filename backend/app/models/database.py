from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

import os

load_dotenv()

USER = os.environ["POSTGRES_USER"]
PASSWORD = os.environ["POSTGRES_PASSWORD"]
HOST = os.environ["POSTGRES_HOST"]
PORT = os.environ["POSTGRES_PORT"]
DATABASE = os.environ["POSTGRES_DB"]

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# dependency injection to get a database session.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# functional session for sessions outside of API request contexts (WS, MQTT)
def get_open_db_session():
    return SessionLocal()
