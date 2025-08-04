from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import auth_controller, user_controller, record_controller, emotion_controller, voice_controller, garden_controller

from database import Base, engine
from models.user import User
from models.record import Record
from models.garden_item import GardenItem, GardenItemTemplate
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(record_controller.router)
app.include_router(emotion_controller.router)
app.include_router(voice_controller.router)
app.include_router(garden_controller.router)

@app.get("/")
def read_root():
    return {"message": "SimLog API is running!"}
