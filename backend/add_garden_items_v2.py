from sqlalchemy.orm import Session
from database import engine, get_db
from models.garden_item import GardenItemTemplate
from datetime import datetime

def add_garden_items_v2():
    print("개선된 정원 아이템들을 추가합니다...")
    
    # 데이터베이스 세션 생성
    db = Session(engine)
    
    try:
        # 개선된 상점 아이템들
        shop_items = [
            # 울타리 (방향별로 구분)
            {
                'item_type': 'fence',
                'item_name': '연한 초록 울타리',
                'item_description': '연한 초록색 울타리 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/colors/light_green/horizontal_regular.png',
                'price': 8,
                'rarity': 'common',
                'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom']
            },
            {
                'item_type': 'fence',
                'item_name': '초록 울타리',
                'item_description': '초록색 울타리 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/colors/green/horizontal_regular.png',
                'price': 8,
                'rarity': 'common',
                'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom']
            },
            {
                'item_type': 'fence',
                'item_name': '이끼 초록 울타리',
                'item_description': '이끼 초록색 울타리 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/colors/moss_green/horizontal_regular.png',
                'price': 12,
                'rarity': 'rare',
                'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom']
            },
            {
                'item_type': 'fence',
                'item_name': '어두운 이끼 초록 울타리',
                'item_description': '어두운 이끼 초록색 울타리 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/colors/dark_moss_green/horizontal_regular.png',
                'price': 15,
                'rarity': 'rare',
                'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom']
            },
            
            # 꽃들
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
            {
                'item_type': 'flower',
                'item_name': '흰 꽃',
                'item_description': '흰색 꽃 - 크기를 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/flowers/white.png',
                'price': 5,
                'rarity': 'common',
                'variants': ['small_paddles', 'big_paddles']
            },
            {
                'item_type': 'flower',
                'item_name': '복숭아 꽃',
                'item_description': '복숭아색 꽃 - 크기를 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/flowers/peach.png',
                'price': 6,
                'rarity': 'rare',
                'variants': ['small_paddles', 'big_paddles']
            },
            {
                'item_type': 'flower',
                'item_name': '파란 꽃',
                'item_description': '파란색 꽃 - 크기를 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/flowers/blue.png',
                'price': 6,
                'rarity': 'rare',
                'variants': ['small_paddles', 'big_paddles']
            },
            
            # 돌담/벽돌
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
            
            # 다리
            {
                'item_type': 'decoration',
                'item_name': '나무 다리',
                'item_description': '자연스러운 나무 다리 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/bridge/bridge_horizontal.png',
                'price': 20,
                'rarity': 'rare',
                'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom']
            },
            
            # 연못
            {
                'item_type': 'decoration',
                'item_name': '연못',
                'item_description': '아름다운 연못 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/pond/pond/pond_center.png',
                'price': 25,
                'rarity': 'epic',
                'variants': ['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right', 'left', 'right', 'top', 'bottom']
            },
            
            # 물고기
            {
                'item_type': 'decoration',
                'item_name': '빨간 물고기',
                'item_description': '귀여운 빨간 물고기',
                'item_image': 'assets/images/garden/fishes/red.png',
                'price': 8,
                'rarity': 'common',
                'variants': []
            },
            {
                'item_type': 'decoration',
                'item_name': '주황 물고기',
                'item_description': '귀여운 주황 물고기',
                'item_image': 'assets/images/garden/fishes/orange.png',
                'price': 8,
                'rarity': 'common',
                'variants': []
            },
            
            # 연꽃
            {
                'item_type': 'flower',
                'item_name': '연꽃',
                'item_description': '아름다운 연꽃 - 색상을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/lotus/light_green.png',
                'price': 12,
                'rarity': 'rare',
                'variants': ['light_green', 'green', 'moss_green', 'dark_moss_green']
            },
            
            # 채소
            {
                'item_type': 'decoration',
                'item_name': '토마토',
                'item_description': '신선한 토마토',
                'item_image': 'assets/images/garden/veggie/single/tomato.png',
                'price': 6,
                'rarity': 'common',
                'variants': []
            },
            {
                'item_type': 'decoration',
                'item_name': '딸기',
                'item_description': '달콤한 딸기',
                'item_image': 'assets/images/garden/veggie/single/strawberry.png',
                'price': 6,
                'rarity': 'common',
                'variants': []
            },
            {
                'item_type': 'decoration',
                'item_name': '당근',
                'item_description': '영양만점 당근',
                'item_image': 'assets/images/garden/veggie/single/carrot.png',
                'price': 5,
                'rarity': 'common',
                'variants': []
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
        print("✅ 모든 정원 아이템 추가가 완료되었습니다!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_garden_items_v2() 