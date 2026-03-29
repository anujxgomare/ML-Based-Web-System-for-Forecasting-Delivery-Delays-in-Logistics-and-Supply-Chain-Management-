from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.prediction_service import predict_and_save

# ✅ THIS LINE IS MANDATORY
router = APIRouter()

@router.post("/predict")
def predict(data: dict, db: Session = Depends(get_db)):
    return predict_and_save(data, db)