#!/usr/bin/env python3
"""
기존 아이템들의 레이어를 새로운 시스템에 맞게 업데이트하는 마이그레이션 스크립트
- 물고기, 새, 나비, 벌: 레이어 2 -> 레이어 3 (동물)
- 기타 아이템들은 기존 로직에 따라 업데이트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models.garden_item import GardenItem, GardenItemTemplate
from services.garden_service import GardenService

def update_item_layers():
    """기존 아이템들의 레이어를 새로운 시스템에 맞게 업데이트"""
    db = SessionLocal()
    
    try:
        print("=== 아이템 레이어 업데이트 시작 ===")
        
        # GardenItem 업데이트
        garden_items = db.query(GardenItem).all()
        updated_count = 0
        
        for item in garden_items:
            old_layer = item.layer
            new_layer = GardenService._get_item_layer(item.item_name)
            
            if old_layer != new_layer:
                print(f"GardenItem 업데이트: {item.item_name} (ID: {item.id}) - 레이어 {old_layer} -> {new_layer}")
                item.layer = new_layer
                updated_count += 1
        
        # GardenItemTemplate 업데이트
        template_items = db.query(GardenItemTemplate).all()
        template_updated_count = 0
        
        for item in template_items:
            old_layer = item.layer
            new_layer = GardenService._get_item_layer(item.item_name)
            
            if old_layer != new_layer:
                print(f"GardenItemTemplate 업데이트: {item.item_name} (ID: {item.id}) - 레이어 {old_layer} -> {new_layer}")
                item.layer = new_layer
                template_updated_count += 1
        
        # 변경사항 저장
        db.commit()
        
        print(f"\n=== 업데이트 완료 ===")
        print(f"GardenItem 업데이트: {updated_count}개")
        print(f"GardenItemTemplate 업데이트: {template_updated_count}개")
        
        # 레이어별 통계 출력
        print(f"\n=== 레이어별 통계 ===")
        layer_stats = {}
        for item in garden_items:
            layer = item.layer
            if layer not in layer_stats:
                layer_stats[layer] = 0
            layer_stats[layer] += 1
        
        for layer in sorted(layer_stats.keys()):
            layer_name = {0: '배경', 1: '중간', 2: '식물', 3: '동물'}.get(layer, f'레이어 {layer}')
            print(f"{layer_name} (레이어 {layer}): {layer_stats[layer]}개")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_item_layers() 