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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기본 엔드포인트
@app.get("/")
def read_root():
    return {"message": "SimLog API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "SimLog API is running!"}

# 단계 1: 기본 컨트롤러만 추가 (오류 발생 시 주석 처리)
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

# 단계 2: 나머지 컨트롤러들 (필요시 주석 해제)
# try:
#     from controllers import record_controller
#     app.include_router(record_controller.router)
#     logging.info("Record controller loaded successfully")
# except Exception as e:
#     logging.warning(f"Record controller failed to load: {e}")

# try:
#     from controllers import emotion_controller
#     app.include_router(emotion_controller.router)
#     logging.info("Emotion controller loaded successfully")
# except Exception as e:
#     logging.warning(f"Emotion controller failed to load: {e}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
