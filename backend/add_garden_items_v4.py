from sqlalchemy.orm import Session
from database import engine, get_db
from models.garden_item import GardenItemTemplate
from datetime import datetime
import os

def add_garden_items_v4():
    print("실제 존재하는 모든 에셋을 기반으로 한 정원 아이템들을 추가합니다...")
    
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
            {
                'item_type': 'flower',
                'item_name': '흰 꽃',
                'item_description': '흰색 꽃 - 크기를 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/flowers/big_paddle/white_small_paddles.png',
                'price': 5,
                'rarity': 'common',
                'variants': ['small_paddles', 'big_paddles']
            },
            {
                'item_type': 'flower',
                'item_name': '복숭아 꽃',
                'item_description': '복숭아색 꽃 - 크기를 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/flowers/big_paddle/peach_small_paddles.png',
                'price': 6,
                'rarity': 'rare',
                'variants': ['small_paddles', 'big_paddles']
            },
            {
                'item_type': 'flower',
                'item_name': '파란 꽃',
                'item_description': '파란색 꽃 - 크기를 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/flowers/big_paddle/blue_small_paddles.png',
                'price': 6,
                'rarity': 'rare',
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
            
            # 울타리 (실제 파일 존재)
            {
                'item_type': 'fence',
                'item_name': '흰색 울타리',
                'item_description': '깔끔한 흰색 울타리 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/fence/white/Direction=↔️ Horizontal, Color=White.png',
                'price': 8,
                'rarity': 'common',
                'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
            },
            {
                'item_type': 'fence',
                'item_name': '연한 나무 울타리',
                'item_description': '자연스러운 연한 나무 울타리 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/fence/light_wood/Direction=↔️ Horizontal, Color=Light Wood.png',
                'price': 8,
                'rarity': 'common',
                'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
            },
            
            # 부시 (실제 파일 존재)
            {
                'item_type': 'decoration',
                'item_name': '연한 초록 부시',
                'item_description': '연한 초록색 부시 - 방향과 크기를 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/bushes/bush/light_green/horizontal_regular.png',
                'price': 6,
                'rarity': 'common',
                'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
            },
            {
                'item_type': 'decoration',
                'item_name': '초록 부시',
                'item_description': '초록색 부시 - 방향과 크기를 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/bushes/bush/green/horizontal_regular.png',
                'price': 6,
                'rarity': 'common',
                'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
            },
            {
                'item_type': 'decoration',
                'item_name': '이끼 초록 부시',
                'item_description': '이끼 초록색 부시 - 방향과 크기를 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/bushes/bush/moss_green/horizontal_regular.png',
                'price': 7,
                'rarity': 'rare',
                'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
            },
            {
                'item_type': 'decoration',
                'item_name': '어두운 이끼 초록 부시',
                'item_description': '어두운 이끼 초록색 부시 - 방향과 크기를 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/bushes/bush/dark_moss_green/horizontal_regular.png',
                'price': 8,
                'rarity': 'rare',
                'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
            },
            
            # 다리 (실제 파일 존재)
            {
                'item_type': 'decoration',
                'item_name': '나무 다리',
                'item_description': '자연스러운 나무 다리 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/bridge/bridge_horizontal.png',
                'price': 20,
                'rarity': 'rare',
                'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom']
            },
            
            # 연못 (실제 파일 존재)
            {
                'item_type': 'decoration',
                'item_name': '연못',
                'item_description': '아름다운 연못 - 방향을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/pond/pond/Direction=🔄 Center.png',
                'price': 25,
                'rarity': 'epic',
                'variants': ['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right', 'left', 'right', 'top', 'bottom']
            },
            
            # 물고기 (실제 파일 존재)
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
            
            # 연꽃 (실제 파일 존재)
            {
                'item_type': 'flower',
                'item_name': '연꽃',
                'item_description': '아름다운 연꽃 - 색상을 선택해서 배치할 수 있습니다',
                'item_image': 'assets/images/garden/lotus/light_green.png',
                'price': 12,
                'rarity': 'rare',
                'variants': ['light_green', 'green', 'moss_green', 'dark_moss_green']
            },
            
            # 채소 (실제 파일 존재)
            {
                'item_type': 'decoration',
                'item_name': '토마토',
                'item_description': '신선한 토마토',
                'item_image': 'assets/images/garden/veggie/single/Type=Tomato.png',
                'price': 6,
                'rarity': 'common',
                'variants': []
            },
            {
                'item_type': 'decoration',
                'item_name': '딸기',
                'item_description': '달콤한 딸기',
                'item_image': 'assets/images/garden/veggie/single/Type=Strawberry.png',
                'price': 6,
                'rarity': 'common',
                'variants': []
            },
            {
                'item_type': 'decoration',
                'item_name': '당근',
                'item_description': '영양만점 당근',
                'item_image': 'assets/images/garden/veggie/single/Type=Carrot.png',
                'price': 5,
                'rarity': 'common',
                'variants': []
            },
            {
                'item_type': 'decoration',
                'item_name': '양파',
                'item_description': '맛있는 양파',
                'item_image': 'assets/images/garden/veggie/single/Type=Onion.png',
                'price': 5,
                'rarity': 'common',
                'variants': []
            },
            {
                'item_type': 'decoration',
                'item_name': '마늘',
                'item_description': '향긋한 마늘',
                'item_image': 'assets/images/garden/veggie/single/Type=Garlic.png',
                'price': 5,
                'rarity': 'common',
                'variants': []
            },
            {
                'item_type': 'decoration',
                'item_name': '오이',
                'item_description': '시원한 오이',
                'item_image': 'assets/images/garden/veggie/single/Type=Cucumber.png',
                'price': 5,
                'rarity': 'common',
                'variants': []
            },
            {
                'item_type': 'decoration',
                'item_name': '체리 토마토',
                'item_description': '작고 귀여운 체리 토마토',
                'item_image': 'assets/images/garden/veggie/single/Type=Cherry Tomatoes.png',
                'price': 6,
                'rarity': 'common',
                'variants': []
            },
            {
                'item_type': 'decoration',
                'item_name': '무',
                'item_description': '새콤달콤한 무',
                'item_image': 'assets/images/garden/veggie/single/Type=Radish.png',
                'price': 5,
                'rarity': 'common',
                'variants': []
            },
            
            # 배경 (실제 파일 존재)
            {
                'item_type': 'background',
                'item_name': '잔디 배경',
                'item_description': '푸른 잔디 배경',
                'item_image': 'assets/images/garden/backgrounds/Options=🌱 Grass.png',
                'price': 30,
                'rarity': 'epic',
                'variants': []
            },
            {
                'item_type': 'background',
                'item_name': '모래 배경',
                'item_description': '따뜻한 모래 배경',
                'item_image': 'assets/images/garden/backgrounds/Options=🏝️ Sand.png',
                'price': 25,
                'rarity': 'rare',
                'variants': []
            },
            {
                'item_type': 'background',
                'item_name': '흙 배경',
                'item_description': '자연스러운 흙 배경',
                'item_image': 'assets/images/garden/backgrounds/Options=🪱 Soil.png',
                'price': 20,
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
        print("✅ 모든 실제 에셋 기반 정원 아이템 추가가 완료되었습니다!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_garden_items_v4() 