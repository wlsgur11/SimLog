from sqlalchemy.orm import Session
from database import engine, get_db
from models.garden_item import GardenItemTemplate
from datetime import datetime
import os

def add_garden_items_v3():
    print("실제 에셋이 있는 정원 아이템들을 추가합니다...")
    
    # 데이터베이스 세션 생성
    db = Session(engine)
    
    try:
        # 실제 존재하는 에셋 파일들만 포함한 상점 아이템들
        shop_items = [
            # 꽃들 (실제 파일 존재)
            {
                'item_type': 'flower',
                'item_name': '노란 꽃',
                'item_description': '노란색 꽃 - 크기를 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/flowers/yellow.png',
                'price': 5,
                'rarity': 'common',
                'variants': ['small_paddles', 'big_paddles']
            },
            {
                'item_type': 'flower',
                'item_name': '보라 꽃',
                'item_description': '보라색 꽃 - 크기를 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/flowers/purple.png',
                'price': 5,
                'rarity': 'common',
                'variants': ['small_paddles', 'big_paddles']
            },
            {
                'item_type': 'flower',
                'item_name': '분홍 꽃',
                'item_description': '분홍색 꽃 - 크기를 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/flowers/pink.png',
                'price': 5,
                'rarity': 'common',
                'variants': ['small_paddles', 'big_paddles']
            },
            
            # 돌담/벽돌 (실제 파일 존재)
            {
                'item_type': 'decoration',
                'item_name': '돌담',
                'item_description': '자연스러운 돌담 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/rocks/rocks.png',
                'price': 10,
                'rarity': 'common',
                'variants': ['horizontal', 'vertical']
            },
            {
                'item_type': 'decoration',
                'item_name': '벽돌',
                'item_description': '정돈된 벽돌 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/rocks/bricks.png',
                'price': 12,
                'rarity': 'rare',
                'variants': ['horizontal', 'vertical']
            },
            {
                'item_type': 'decoration',
                'item_name': '원형 벽돌',
                'item_description': '둥근 벽돌 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/rocks/circle_bricks.png',
                'price': 15,
                'rarity': 'rare',
                'variants': ['horizontal', 'vertical']
            },
            
            # 흰색 울타리 (실제 파일 존재)
            {
                'item_type': 'fence',
                'item_name': '흰색 울타리',
                'item_description': '깔끔한 흰색 울타리 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/fence/white/Direction=↔️ Horizontal, Color=White.png',
                'price': 8,
                'rarity': 'common',
                'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
            },
            
            # 연한 나무 울타리 (실제 파일 존재)
            {
                'item_type': 'fence',
                'item_name': '연한 나무 울타리',
                'item_description': '자연스러운 연한 나무 울타리 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/fence/light_wood/Direction=↔️ Horizontal, Color=Light Wood.png',
                'price': 8,
                'rarity': 'common',
                'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
            },
        ]
        
        # 기존 아이템 확인 후 추가
        for item_data in shop_items:
            existing = db.query(GardenItemTemplate).filter(
                GardenItemTemplate.item_name == item_data['item_name']
            ).first()
            
            if not existing:
                # variants 필드는 별도로 저장하지 않고, 아이템 설명에 포함
                template_data = {k: v for k, v in item_data.items() if k != 'variants'}
                template = GardenItemTemplate(**template_data)
                db.add(template)
                print(f"✓ 추가됨: {item_data['item_name']} ({item_data['price']} 씨앗)")
            else:
                print(f"⚠ 이미 존재함: {item_data['item_name']}")
        
        db.commit()
        print("✅ 실제 에셋이 있는 정원 아이템 추가가 완료되었습니다!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_garden_items_v3() 