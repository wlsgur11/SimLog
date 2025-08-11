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

# 단계별로 컨트롤러 추가 예정
# app.include_router(auth_controller.router)
# app.include_router(user_controller.router)
# app.include_router(record_controller.router)
# app.include_router(emotion_controller.router)
# app.include_router(voice_controller.router)
# app.include_router(garden_controller.router)
# app.include_router(reports_controller.router)
# app.include_router(alerts_controller.router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
