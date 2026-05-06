from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST     = os.getenv("MYSQLHOST") or os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("MYSQLPORT") or os.getenv("DB_PORT", "3306")
DB_NAME     = os.getenv("MYSQLDATABASE") or os.getenv("DB_NAME", "courier_track")
DB_USER     = os.getenv("MYSQLUSER") or os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("MYSQLPASSWORD") or os.getenv("DB_PASSWORD", "")

# quote_plus encodes special characters like @ in password
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
