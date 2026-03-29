from fastapi import FastAPI
from app.routes import predict, upload

# ✅ THIS LINE IS REQUIRED
app = FastAPI()

# Include routes
app.include_router(predict.router)
app.include_router(upload.router)

@app.get("/")
def home():
    return {"message": "API is running"}



## python -m uvicorn main:app --reload