from sqlalchemy import Column, Integer, Float, String, TIMESTAMP
from sqlalchemy.sql import func
from app.database.db import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    distance = Column(Float)
    carrier = Column(String(50))
    weather = Column(String(50))
    prediction = Column(Integer)
    probability = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())