from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime


DATABASE_URL = "sqlite:///./surveillance.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine
)

Base = declarative_base()


class TrackingRecord(Base):

    __tablename__ = "tracking_records"

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer)
    object_type = Column(String)
    camera_id = Column(String)
    timestamp = Column(DateTime, default=datetime.now)
    latitude = Column(Float)
    longitude = Column(Float)


Base.metadata.create_all(bind=engine)