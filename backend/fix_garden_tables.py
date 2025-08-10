#!/usr/bin/env python3
"""
마음 정원 테이블 구조 수정 스크립트
현재 잘못된 구조를 코드 모델에 맞게 수정합니다.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from database import Base, engine

def fix_garden_tables():
    """마음 정원 테이블 구조를 수정합니다."""
    print("🔧 마음 정원 테이블 구조 수정을 시작합니다...")
    
    try:
        with engine.connect() as conn:
            print("✅ 데이터베이스 연결 성공")
            
            # 1. 기존 테이블 백업 (선택사항)
            print("📋 기존 테이블 백업 중...")
            try:
                conn.execute(text("CREATE TABLE garden_items_backup AS SELECT * FROM garden_items"))
                conn.execute(text("CREATE TABLE garden_item_templates_backup AS SELECT * FROM garden_item_templates"))
                print("   - 백업 테이블 생성 완료")
            except Exception as e:
                print(f"   - 백업 실패 (이미 존재할 수 있음): {e}")
            
            # 2. 기존 테이블 삭제
            print("🗑️  기존 테이블 삭제 중...")
            conn.execute(text("DROP TABLE IF EXISTS garden_items"))
            conn.execute(text("DROP TABLE IF EXISTS garden_item_templates"))
            print("   - 기존 테이블 삭제 완료")
            
            # 3. 새로운 테이블 생성
            print("🔨 새로운 테이블 생성 중...")
            
            # garden_item_templates 테이블 생성
            conn.execute(text("""
                CREATE TABLE garden_item_templates (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    item_type VARCHAR(50) NOT NULL,
                    item_name VARCHAR(100) NOT NULL,
                    item_description VARCHAR(500),
                    item_image VARCHAR(255),
                    price INT NOT NULL,
                    rarity VARCHAR(20) DEFAULT 'common',
                    layer INT DEFAULT 0,
                    is_available BOOLEAN DEFAULT TRUE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """))
            print("   - garden_item_templates 테이블 생성 완료")
            
            # garden_items 테이블 생성
            conn.execute(text("""
                CREATE TABLE garden_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    item_type VARCHAR(50) NOT NULL,
                    item_name VARCHAR(100) NOT NULL,
                    item_image VARCHAR(255),
                    position_x INT DEFAULT 0,
                    position_y INT DEFAULT 0,
                    layer INT DEFAULT 0,
                    is_equipped BOOLEAN DEFAULT FALSE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """))
            print("   - garden_items 테이블 생성 완료")
            
            # 4. 인덱스 생성
            print("📊 인덱스 생성 중...")
            conn.execute(text("CREATE INDEX idx_garden_items_user_id ON garden_items(user_id)"))
            conn.execute(text("CREATE INDEX idx_garden_items_equipped ON garden_items(is_equipped)"))
            conn.execute(text("CREATE INDEX idx_garden_item_templates_type ON garden_item_templates(item_type)"))
            conn.execute(text("CREATE INDEX idx_garden_item_templates_available ON garden_item_templates(is_available)"))
            print("   - 인덱스 생성 완료")
            
            # 5. 기본 아이템 템플릿 데이터 삽입
            print("🌱 기본 아이템 템플릿 데이터 삽입 중...")
            
            # 배경 아이템들
            background_items = [
                ("background", "잔디", "초록색 잔디", "assets/images/garden/background/grass.png", 5, "common", 0),
                ("background", "모래", "황금빛 모래", "assets/images/garden/background/sand.png", 5, "common", 0),
                ("background", "흙", "갈색 흙", "assets/images/garden/background/soil.png", 5, "common", 0)
            ]
            
            # 물 관련 아이템들
            water_items = [
                ("water", "연못", "고요한 연못", "assets/images/garden/pond/pond/Direction=🔄 Center.png", 15, "rare", 1),
                ("water", "시냇물", "맑은 시냇물", "assets/images/garden/water/stream.png", 10, "common", 1)
            ]
            
            # 식물 아이템들
            plant_items = [
                ("plant", "꽃", "아름다운 꽃", "assets/images/garden/flowers/flower.png", 8, "common", 2),
                ("plant", "나무", "푸른 나무", "assets/images/garden/trees/tree.png", 12, "rare", 2),
                ("plant", "부시", "초록 부시", "assets/images/garden/bushes/bush.png", 6, "common", 2)
            ]
            
            # 장식 아이템들
            decoration_items = [
                ("decoration", "울타리", "나무 울타리", "assets/images/garden/fence/fence.png", 10, "common", 2),
                ("decoration", "다리", "나무 다리", "assets/images/garden/bridge/bridge.png", 15, "rare", 2),
                ("decoration", "벤치", "휴식용 벤치", "assets/images/garden/decorations/bench.png", 20, "epic", 2)
            ]
            
            all_items = background_items + water_items + plant_items + decoration_items
            
            for item in all_items:
                conn.execute(text("""
                    INSERT INTO garden_item_templates 
                    (item_type, item_name, item_description, item_image, price, rarity, layer) 
                    VALUES (:item_type, :item_name, :item_description, :item_image, :price, :rarity, :layer)
                """), {
                    "item_type": item[0],
                    "item_name": item[1], 
                    "item_description": item[2],
                    "item_image": item[3],
                    "price": item[4],
                    "rarity": item[5],
                    "layer": item[6]
                })
            
            print(f"   - {len(all_items)}개의 기본 아이템 템플릿 추가 완료")
            
            conn.commit()
            print("✅ 모든 변경사항이 저장되었습니다")
            
            # 6. 최종 확인
            print("🔍 테이블 구조 확인 중...")
            result = conn.execute(text("SHOW TABLES LIKE 'garden%'"))
            tables = [row[0] for row in result]
            print(f"   - 정원 관련 테이블: {', '.join(tables)}")
            
            # garden_items 구조 확인
            result = conn.execute(text("DESCRIBE garden_items"))
            print("   - garden_items 컬럼:")
            for row in result:
                print(f"     {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")
            
            # garden_item_templates 구조 확인
            result = conn.execute(text("DESCRIBE garden_item_templates"))
            print("   - garden_item_templates 컬럼:")
            for row in result:
                print(f"     {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")
            
    except OperationalError as e:
        print(f"❌ 데이터베이스 연결 실패: {e}")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False
    
    print("🎉 마음 정원 테이블 구조 수정이 완료되었습니다!")
    return True

if __name__ == "__main__":
    # .env 파일 로드
    load_dotenv()
    
    # 사용자 확인
    print("⚠️  경고: 이 작업은 기존 정원 데이터를 모두 삭제합니다!")
    print("백업 테이블이 생성되지만, 원본 데이터는 복구할 수 없습니다.")
    confirm = input("계속하시겠습니까? (yes/no): ")
    
    if confirm.lower() == "yes":
        fix_garden_tables()
    else:
        print("❌ 작업이 취소되었습니다.")
