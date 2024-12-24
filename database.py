import os
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from dotenv import load_dotenv
from models import Event

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mariawasnotfound:0000@db:5432/afisha_db")

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def save_event(name, date, time, location, latitude, longitude):
    db: Session = SessionLocal()
    try:
        new_event = Event(
            name=name,
            date=date,
            time=time,
            location=location,
            latitude=latitude,
            longitude=longitude
        )
        db.add(new_event)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ошибка при сохранении события: {e}")
    finally:
        db.close()

def get_session():
   return SessionLocal()
