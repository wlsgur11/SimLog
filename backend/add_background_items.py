#!/usr/bin/env python3
"""
배경 아이템들을 상점에 추가하는 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.garden_item import GardenItemTemplate
from sqlalchemy import text

def add_background_items():
    """배경 아이템들을 상점에 추가"""
    
    db = SessionLocal()
    try:
        # 기존 배경 아이템이 있는지 확인
        existing_items = db.query(GardenItemTemplate).filter(
            GardenItemTemplate.item_name.like('%잔디%')
        ).first()
        
        if existing_items:
            print("배경 아이템들이 이미 존재합니다.")
            return
        
        # 배경 아이템들 추가
        background_items = [
            {
                'item_type': 'background',
                'item_name': '잔디',
                'item_description': '푸른 잔디 배경입니다. 정원의 기본 배경으로 사용할 수 있습니다.',
                'item_image': 'assets/images/garden/background/grass.png',
                'price': 5,
                'rarity': 'common',
                'layer': 0
            },
            {
                'item_type': 'background',
                'item_name': '모래',
                'item_description': '황금빛 모래 배경입니다. 사막 테마의 정원을 만들 수 있습니다.',
                'item_image': 'assets/images/garden/background/sand.png',
                'price': 5,
                'rarity': 'common',
                'layer': 0
            },
            {
                'item_type': 'background',
                'item_name': '돌',
                'item_description': '회색 돌 배경입니다. 산악 테마의 정원을 만들 수 있습니다.',
                'item_image': 'assets/images/garden/background/stone.png',
                'price': 8,
                'rarity': 'common',
                'layer': 0
            },
            {
                'item_type': 'background',
                'item_name': '자갈',
                'item_description': '작은 자갈 배경입니다. 일본식 정원을 만들 수 있습니다.',
                'item_image': 'assets/images/garden/background/gravel.png',
                'price': 6,
                'rarity': 'common',
                'layer': 0
            },
            {
                'item_type': 'background',
                'item_name': '흙',
                'item_description': '갈색 흙 배경입니다. 자연스러운 정원을 만들 수 있습니다.',
                'item_image': 'assets/images/garden/background/dirt.png',
                'price': 3,
                'rarity': 'common',
                'layer': 0
            }
        ]
        
        for item_data in background_items:
            new_item = GardenItemTemplate(**item_data)
            db.add(new_item)
            print(f"✅ {item_data['item_name']} 추가됨")
        
        db.commit()
        print("🎉 모든 배경 아이템이 성공적으로 추가되었습니다!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 배경 아이템 추가 실패: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_background_items() 