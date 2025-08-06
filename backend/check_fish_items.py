#!/usr/bin/env python3
"""
데이터베이스에서 물고기 아이템들을 확인하는 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.garden_item import GardenItem, GardenItemTemplate
from services.garden_service import GardenService

def check_fish_items():
    """데이터베이스에서 물고기 아이템들을 확인"""
    db = SessionLocal()
    
    try:
        print("=== GardenItem 테이블의 물고기 아이템들 ===")
        fish_items = db.query(GardenItem).filter(GardenItem.item_name.contains('물고기')).all()
        
        if not fish_items:
            print("GardenItem 테이블에 물고기 아이템이 없습니다.")
        else:
            for item in fish_items:
                expected_layer = GardenService._get_item_layer(item.item_name)
                print(f"ID: {item.id}, Name: '{item.item_name}', Current Layer: {item.layer}, Expected Layer: {expected_layer}")
        
        print("\n=== GardenItemTemplate 테이블의 물고기 아이템들 ===")
        fish_templates = db.query(GardenItemTemplate).filter(GardenItemTemplate.item_name.contains('물고기')).all()
        
        if not fish_templates:
            print("GardenItemTemplate 테이블에 물고기 아이템이 없습니다.")
        else:
            for item in fish_templates:
                expected_layer = GardenService._get_item_layer(item.item_name)
                print(f"ID: {item.id}, Name: '{item.item_name}', Current Layer: {item.layer}, Expected Layer: {expected_layer}")
        
        print("\n=== 모든 물고기 관련 아이템들 (부분 일치) ===")
        all_fish_related = db.query(GardenItem).filter(
            GardenItem.item_name.like('%물고기%')
        ).all()
        
        for item in all_fish_related:
            expected_layer = GardenService._get_item_layer(item.item_name)
            print(f"ID: {item.id}, Name: '{item.item_name}', Current Layer: {item.layer}, Expected Layer: {expected_layer}")
            
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_fish_items() 