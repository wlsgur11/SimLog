from fastapi import FastAPI
from controllers import auth_controller, user_controller, record_controller, emotion_controller, voice_controller

from database import Base, engine
from models.user import User
from models.record import Record
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(record_controller.router)
app.include_router(emotion_controller.router)
app.include_router(voice_controller.router)

@app.get("/")
def read_root():
    return {"message": "SimLog API is running!"}

@app.get("/debug/env")
def debug_env():
    """환경 변수 디버깅용 (개발 환경에서만 사용)"""
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "NOT_SET")[:10] + "..." if os.getenv("OPENAI_API_KEY") else "NOT_SET",
        "CLOVA_CLIENT_ID": os.getenv("CLOVA_CLIENT_ID", "NOT_SET"),
        "SECRET_KEY": os.getenv("SECRET_KEY", "NOT_SET")[:10] + "..." if os.getenv("SECRET_KEY") else "NOT_SET"
    }