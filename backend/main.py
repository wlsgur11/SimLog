from fastapi import FastAPI
import os
import logging
from sqlalchemy import text
from database import Base, engine

# 기본 모델들만 먼저 import
try:
    from models.user import User
    logging.info("User model imported successfully")
except Exception as e:
    logging.error(f"Failed to import User model: {e}")
    User = None

try:
    from models.record import Record
    logging.info("Record model imported successfully")
except Exception as e:
    logging.error(f"Failed to import Record model: {e}")
    Record = None

try:
    from models.garden_item import GardenItem, GardenItemTemplate
    logging.info("Garden models imported successfully")
except Exception as e:
    logging.error(f"Failed to import Garden models: {e}")
    GardenItem = None
    GardenItemTemplate = None

# 추가 모델들은 나중에 import (존재하는 것만)
additional_models = []
try:
    from models.user_consent import UserConsent
    additional_models.append(UserConsent.__table__)
    logging.info("UserConsent model imported successfully")
except Exception as e:
    logging.warning(f"Failed to import UserConsent model: {e}")

try:
    from models.weekly_summary import WeeklySummaryCache
    additional_models.append(WeeklySummaryCache.__table__)
    logging.info("WeeklySummaryCache model imported successfully")
except Exception as e:
    logging.warning(f"Failed to import WeeklySummaryCache model: {e}")

# 실제로는 garden_item_templates와 garden_items를 사용
# shop_items, user_inventory는 별도 테이블이 아님
logging.info("Shop and inventory use garden_item_templates and garden_items tables")

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)  # DEBUG 레벨로 변경

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
    # 데이터베이스 연결 테스트
    with engine.connect() as connection:
        logging.info("Database connection successful")
        
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    logging.info("Database tables created successfully")
    
    # 테이블 존재 확인
    with engine.connect() as connection:
        result = connection.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        logging.info(f"Existing tables: {tables}")
        
        # 필요한 모든 테이블 생성
        required_tables = []
        
        # 기본 테이블들 (반드시 필요)
        if User:
            required_tables.append(User.__table__)
        if Record:
            required_tables.append(Record.__table__)
        if GardenItem:
            required_tables.append(GardenItem.__table__)
        if GardenItemTemplate:
            required_tables.append(GardenItemTemplate.__table__)
        
        # 추가 테이블들
        required_tables.extend(additional_models)
        
        for table in required_tables:
            if table and table.name not in tables:
                logging.warning(f"Table {table.name} not found, creating...")
                try:
                    Base.metadata.create_all(bind=engine, tables=[table])
                    logging.info(f"Table {table.name} created successfully")
                except Exception as e:
                    logging.error(f"Failed to create table {table.name}: {e}")
        
        # 상점 데이터 초기화 (필요시)
        try:
            # 상점 관련 테이블이 있는지 확인 (garden_item_templates 사용)
            if 'garden_item_templates' in tables:
                result = connection.execute(text("SELECT COUNT(*) FROM garden_item_templates"))
                shop_item_count = result.scalar()
                
                if shop_item_count == 0:
                    logging.info("Shop is empty, initializing with default items...")
                    # 기본 상점 아이템 추가
                    _initialize_shop_items(connection)
                    logging.info("Shop initialization completed")
                else:
                    logging.info(f"Shop has {shop_item_count} items")
            else:
                logging.info("Shop table (garden_item_templates) not found, will be created during table creation")
                
        except Exception as e:
            logging.warning(f"Shop initialization check failed: {e}")
        
except Exception as e:
    logging.error(f"Database initialization failed: {e}")
    logging.error(f"Error type: {type(e)}")
    # 데이터베이스 연결 실패해도 앱은 실행되도록 함

def _initialize_shop_items(connection):
    """상점에 기본 아이템들을 추가"""
    try:
        # 기본 상점 아이템들
        items = [
            ("background", "잔디 배경", "자연스러운 잔디 배경", "assets/images/garden/backgrounds/Options=🌱 Grass.png", 1, "common", 0),
            ("background", "모래 배경", "따뜻한 모래 배경", "assets/images/garden/backgrounds/Options=🏝️ Sand.png", 1, "common", 0),
            ("background", "흙 배경", "비옥한 흙 배경", "assets/images/garden/backgrounds/Options=🪱 Soil.png", 1, "common", 0),
            ("water", "연못", "아름다운 연못", "assets/images/garden/pond/pond/Direction=🔄 Center.png", 15, "common", 1),
            ("decoration", "노란 꽃", "밝은 노란 꽃", "assets/images/garden/flowers/yellow.png", 1, "common", 2),
            ("decoration", "보라 꽃", "우아한 보라 꽃", "assets/images/garden/flowers/purple.png", 1, "common", 2),
            ("decoration", "분홍 꽃", "사랑스러운 분홍 꽃", "assets/images/garden/flowers/pink.png", 1, "common", 2),
            ("bush", "연한 초록 부시", "자연스러운 연한 초록 부시", "assets/images/garden/bushes/bush/light_green/horizontal_regular.png", 5, "common", 2),
            ("bush", "초록 부시", "자연스러운 초록 부시", "assets/images/garden/bushes/bush/green/horizontal_regular.png", 5, "common", 2),
            ("decoration", "흰 울타리", "깔끔한 흰 울타리", "assets/images/garden/fence/white/Direction=↔️ Horizontal, Color=White.png", 5, "common", 2),
            ("decoration", "나무 다리", "자연스러운 나무 다리", "assets/images/garden/bridge/bridge_horizontal.png", 5, "common", 2),
            ("decoration", "주황 물고기", "귀여운 주황 물고기", "assets/images/garden/fishes/orange.png", 5, "common", 2),
            ("decoration", "딸기", "달콤한 딸기", "assets/images/garden/veggie/single/Type=Strawberry.png", 1, "common", 2),
            ("decoration", "토마토", "신선한 토마토", "assets/images/garden/veggie/single/Type=Tomato.png", 1, "common", 2),
            ("decoration", "당근", "달콤한 당근", "assets/images/garden/veggie/single/Type=Carrot.png", 1, "common", 2)
        ]
        
        for item_type, item_name, item_description, item_image, price, rarity, layer in items:
            connection.execute(text("""
                INSERT INTO garden_item_templates 
                (item_type, item_name, item_description, item_image, price, rarity, layer, is_available, created_at)
                VALUES (:item_type, :item_name, :item_description, :item_image, :price, :rarity, :layer, :is_available, NOW())
            """), {
                "item_type": item_type,
                "item_name": item_name,
                "item_description": item_description,
                "item_image": item_image,
                "price": price,
                "rarity": rarity,
                "layer": layer,
                "is_available": True
            })
        
        connection.commit()
        logging.info(f"Added {len(items)} items to shop")
        
    except Exception as e:
        logging.error(f"Failed to initialize shop items: {e}")
        connection.rollback()

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
