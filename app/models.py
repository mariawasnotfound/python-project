from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    time = Column(DateTime)
    seats_available = Column(Boolean, default=True)
