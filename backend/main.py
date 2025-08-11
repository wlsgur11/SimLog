from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from controllers import auth_controller, user_controller, record_controller, emotion_controller, voice_controller, garden_controller
from controllers import reports_controller, alerts_controller

from database import Base, engine
from models.user import User
from models.record import Record
from models.garden_item import GardenItem, GardenItemTemplate
from models.weekly_summary import WeeklySummaryCache
from models.shared_report import SharedReport
from models.user_consent import UserConsent
from models.alert_state import UserAlertState
import os
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)

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
app.include_router(reports_controller.router)
app.include_router(alerts_controller.router)

@app.on_event("startup")
def seed_on_startup():
    # 개발용 더미 데이터 시드 (옵션)
    if os.environ.get("SIMLOG_DEV_SEED_WEEK") == "1":
        try:
            from dev_seed import seed_weekly_cache, seed_weekly_records
            # 기본: user_id=1에 7일 우울 캐시
            user_id = int(os.environ.get("SIMLOG_DEV_SEED_USER", "1"))
            period = int(os.environ.get("SIMLOG_DEV_SEED_PERIOD", "7"))
            seed_weekly_cache(user_id=user_id, period_days=period)
            seed_weekly_records(user_id=user_id, period_days=period)
            logging.info(f"Dev seed weekly cache done for user_id={user_id}, period={period}")
        except Exception as e:
            logging.warning(f"Dev seed failed: {e}")

@app.get("/")
def read_root():
    return {"message": "SimLog API is running!"}

# Railway 배포를 위한 서버 실행 코드
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
