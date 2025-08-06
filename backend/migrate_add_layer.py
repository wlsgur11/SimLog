#!/usr/bin/env python3
"""
데이터베이스 마이그레이션: GardenItem에 layer 컬럼 추가
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, SessionLocal
from models.garden_item import GardenItem, GardenItemTemplate
from sqlalchemy import text

def migrate_add_layer():
    """GardenItem 테이블에 layer 컬럼 추가"""
    
    db = SessionLocal()
    try:
        # 1. layer 컬럼 추가
        print("1. GardenItem 테이블에 layer 컬럼 추가 중...")
        db.execute(text("ALTER TABLE garden_items ADD COLUMN layer INTEGER DEFAULT 0"))
        
        # 2. GardenItemTemplate 테이블에 layer 컬럼 추가
        print("2. GardenItemTemplate 테이블에 layer 컬럼 추가 중...")
        db.execute(text("ALTER TABLE garden_item_templates ADD COLUMN layer INTEGER DEFAULT 0"))
        
        # 3. 기존 아이템들의 layer 설정
        print("3. 기존 아이템들의 layer 설정 중...")
        
        # 배경 아이템들 (잔디, 모래 등)
        background_items = [
            '잔디', '모래', '흙', '돌', '자갈'
        ]
        
        for item_name in background_items:
            db.execute(text("""
                UPDATE garden_items 
                SET layer = 0 
                WHERE item_name LIKE :pattern
            """), {"pattern": f"%{item_name}%"})
            
            db.execute(text("""
                UPDATE garden_item_templates 
                SET layer = 0 
                WHERE item_name LIKE :pattern
            """), {"pattern": f"%{item_name}%"})
        
        # 물 관련 아이템들 (연못, 물 등)
        water_items = [
            '연못', '물', '시냇물', '분수'
        ]
        
        for item_name in water_items:
            db.execute(text("""
                UPDATE garden_items 
                SET layer = 1 
                WHERE item_name LIKE :pattern
            """), {"pattern": f"%{item_name}%"})
            
            db.execute(text("""
                UPDATE garden_item_templates 
                SET layer = 1 
                WHERE item_name LIKE :pattern
            """), {"pattern": f"%{item_name}%"})
        
        # 장식 아이템들 (울타리, 다리 등)
        decoration_items = [
            '울타리', '다리', '벤치', '등불', '문'
        ]
        
        for item_name in decoration_items:
            db.execute(text("""
                UPDATE garden_items 
                SET layer = 1 
                WHERE item_name LIKE :pattern
            """), {"pattern": f"%{item_name}%"})
            
            db.execute(text("""
                UPDATE garden_item_templates 
                SET layer = 1 
                WHERE item_name LIKE :pattern
            """), {"pattern": f"%{item_name}%"})
        
        # 식물 아이템들 (꽃, 나무, 채소 등)
        plant_items = [
            '꽃', '나무', '부시', '채소', '연꽃', '토마토', '딸기', '당근', '양파', '마늘', '오이', '무'
        ]
        
        for item_name in plant_items:
            db.execute(text("""
                UPDATE garden_items 
                SET layer = 2 
                WHERE item_name LIKE :pattern
            """), {"pattern": f"%{item_name}%"})
            
            db.execute(text("""
                UPDATE garden_item_templates 
                SET layer = 2 
                WHERE item_name LIKE :pattern
            """), {"pattern": f"%{item_name}%"})
        
        # 동물 아이템들 (물고기, 새 등)
        animal_items = [
            '물고기', '새', '나비', '벌'
        ]
        
        for item_name in animal_items:
            db.execute(text("""
                UPDATE garden_items 
                SET layer = 2 
                WHERE item_name LIKE :pattern
            """), {"pattern": f"%{item_name}%"})
            
            db.execute(text("""
                UPDATE garden_item_templates 
                SET layer = 2 
                WHERE item_name LIKE :pattern
            """), {"pattern": f"%{item_name}%"})
        
        db.commit()
        print("✅ 마이그레이션 완료!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 마이그레이션 실패: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    migrate_add_layer() 