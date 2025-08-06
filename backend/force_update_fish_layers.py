#!/usr/bin/env python3
"""
물고기 아이템들의 레이어를 강제로 레이어 3으로 업데이트하는 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.garden_item import GardenItem, GardenItemTemplate

def force_update_fish_layers():
    """물고기 아이템들의 레이어를 강제로 레이어 3으로 업데이트"""
    db = SessionLocal()
    
    try:
        print("=== 물고기 아이템 레이어 강제 업데이트 시작 ===")
        
        # GardenItem에서 물고기 아이템들 찾기
        fish_items = db.query(GardenItem).filter(
            GardenItem.item_name.like('%물고기%')
        ).all()
        
        updated_count = 0
        for item in fish_items:
            if item.layer != 3:
                print(f"GardenItem 업데이트: {item.item_name} (ID: {item.id}) - 레이어 {item.layer} -> 3")
                item.layer = 3
                updated_count += 1
            else:
                print(f"GardenItem 이미 올바름: {item.item_name} (ID: {item.id}) - 레이어 {item.layer}")
        
        # GardenItemTemplate에서 물고기 아이템들 찾기
        fish_templates = db.query(GardenItemTemplate).filter(
            GardenItemTemplate.item_name.like('%물고기%')
        ).all()
        
        template_updated_count = 0
        for item in fish_templates:
            if item.layer != 3:
                print(f"GardenItemTemplate 업데이트: {item.item_name} (ID: {item.id}) - 레이어 {item.layer} -> 3")
                item.layer = 3
                template_updated_count += 1
            else:
                print(f"GardenItemTemplate 이미 올바름: {item.item_name} (ID: {item.id}) - 레이어 {item.layer}")
        
        # 변경사항 저장
        db.commit()
        
        print(f"\n=== 업데이트 완료 ===")
        print(f"GardenItem 업데이트: {updated_count}개")
        print(f"GardenItemTemplate 업데이트: {template_updated_count}개")
        
        # 업데이트 후 확인
        print(f"\n=== 업데이트 후 확인 ===")
        all_fish = db.query(GardenItem).filter(
            GardenItem.item_name.like('%물고기%')
        ).all()
        
        for item in all_fish:
            print(f"확인: {item.item_name} (ID: {item.id}) - 레이어 {item.layer}")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    force_update_fish_layers() 