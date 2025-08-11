from fastapi import FastAPI
import os
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# CORS 설정 추가
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 기본 엔드포인트
@app.get("/")
def read_root():
    return {"message": "SimLog API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "SimLog API is running!"}

# 데이터베이스 초기화 (오류 처리 포함)
try:
    from database import Base, engine
    Base.metadata.create_all(bind=engine)
    logging.info("Database tables created successfully")
except Exception as e:
    logging.warning(f"Database initialization failed: {e}")
    # 데이터베이스 연결 실패해도 앱은 실행되도록 함

# 단계 1: 기본 컨트롤러 (이미 성공한 것들)
try:
    from controllers import auth_controller
    app.include_router(auth_controller.router)
    logging.info("Auth controller loaded successfully")
except Exception as e:
    logging.warning(f"Auth controller failed to load: {e}")

try:
    from controllers import user_controller
    app.include_router(user_controller.router)
    logging.info("User controller loaded successfully")
except Exception as e:
    logging.warning(f"User controller failed to load: {e}")

# 단계 2: 핵심 기능 컨트롤러
try:
    from controllers import record_controller
    app.include_router(record_controller.router)
    logging.info("Record controller loaded successfully")
except Exception as e:
    logging.warning(f"Record controller failed to load: {e}")

try:
    from controllers import emotion_controller
    app.include_router(emotion_controller.router)
    logging.info("Emotion controller loaded successfully")
except Exception as e:
    logging.warning(f"Emotion controller failed to load: {e}")

try:
    from controllers import voice_controller
    app.include_router(voice_controller.router)
    logging.info("Voice controller loaded successfully")
except Exception as e:
    logging.warning(f"Voice controller failed to load: {e}")

# 단계 3: 정원 및 부가 기능 컨트롤러
try:
    from controllers import garden_controller
    app.include_router(garden_controller.router)
    logging.info("Garden controller loaded successfully")
except Exception as e:
    logging.warning(f"Garden controller failed to load: {e}")

try:
    from controllers import reports_controller
    app.include_router(reports_controller.router)
    logging.info("Reports controller loaded successfully")
except Exception as e:
    logging.warning(f"Reports controller failed to load: {e}")

try:
    from controllers import alerts_controller
    app.include_router(alerts_controller.router)
    logging.info("Alerts controller loaded successfully")
except Exception as e:
    logging.warning(f"Alerts controller failed to load: {e}")

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

# Railway 배포를 위한 서버 실행 코드
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
