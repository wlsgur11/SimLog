#!/usr/bin/env python3
"""
모든 정원 아이템을 데이터베이스에 추가하는 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.garden_item import GardenItemTemplate

def add_all_garden_items():
    db = SessionLocal()
    
    # 기존 아이템들 삭제
    db.query(GardenItemTemplate).delete()
    db.commit()
    
    # 모든 아이템 정의
    shop_items = [
        # 꽃들 (기존)
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
            'price': 5,
            'rarity': 'common',
            'variants': ['small_paddles', 'big_paddles']
        },
        {
            'item_type': 'flower',
            'item_name': '파란 꽃',
            'item_description': '파란색 꽃 - 크기를 선택해서 배치할 수 있습니다',
            'item_image': 'assets/images/garden/flowers/big_paddle/blue_small_paddles.png',
            'price': 5,
            'rarity': 'common',
            'variants': ['small_paddles', 'big_paddles']
        },
        
        # Bloom (새로 추가)
        {
            'item_type': 'bloom',
            'item_name': '노란 꽃봉오리',
            'item_description': '노란색 꽃봉오리 - 크기를 선택해서 배치할 수 있습니다',
            'item_image': 'assets/images/garden/bloom/color/Size=Bud, Color=Yellow.png',
            'price': 4,
            'rarity': 'common',
            'variants': ['bud', 'big_bud', 'flower']
        },
        {
            'item_type': 'bloom',
            'item_name': '보라 꽃봉오리',
            'item_description': '보라색 꽃봉오리 - 크기를 선택해서 배치할 수 있습니다',
            'item_image': 'assets/images/garden/bloom/color/Size=Bud, Color=Purple.png',
            'price': 4,
            'rarity': 'common',
            'variants': ['bud', 'big_bud', 'flower']
        },
        {
            'item_type': 'bloom',
            'item_name': '분홍 꽃봉오리',
            'item_description': '분홍색 꽃봉오리 - 크기를 선택해서 배치할 수 있습니다',
            'item_image': 'assets/images/garden/bloom/color/Size=Bud, Color=Pink.png',
            'price': 4,
            'rarity': 'common',
            'variants': ['bud', 'big_bud', 'flower']
        },
        {
            'item_type': 'bloom',
            'item_name': '복숭아 꽃봉오리',
            'item_description': '복숭아색 꽃봉오리 - 크기를 선택해서 배치할 수 있습니다',
            'item_image': 'assets/images/garden/bloom/color/Size=Bud, Color=Peach.png',
            'price': 4,
            'rarity': 'common',
            'variants': ['bud', 'big_bud', 'flower']
        },
        
        # 장식품들 (기존)
        {
            'item_type': 'decoration',
            'item_name': '돌담',
            'item_description': '자연스러운 돌담',
            'item_image': 'assets/images/garden/rocks/rocks.png',
            'price': 10,
            'rarity': 'common'
        },
        {
            'item_type': 'decoration',
            'item_name': '벽돌',
            'item_description': '정돈된 벽돌',
            'item_image': 'assets/images/garden/rocks/bricks.png',
            'price': 10,
            'rarity': 'common'
        },
        {
            'item_type': 'decoration',
            'item_name': '원형 벽돌',
            'item_description': '원형으로 배치된 벽돌',
            'item_image': 'assets/images/garden/rocks/circle_bricks.png',
            'price': 15,
            'rarity': 'rare'
        },
        
        # 울타리들 (기존 + 흰색 추가)
        {
            'item_type': 'fence',
            'item_name': '흰색 울타리',
            'item_description': '깔끔한 흰색 울타리',
            'item_image': 'assets/images/garden/fence/white/Direction=↔️ Horizontal, Color=White.png',
            'price': 8,
            'rarity': 'common',
            'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
        },
        {
            'item_type': 'fence',
            'item_name': '연한 나무 울타리',
            'item_description': '자연스러운 연한 나무 울타리',
            'item_image': 'assets/images/garden/fence/light_wood/Direction=↔️ Horizontal, Color=Light Wood.png',
            'price': 8,
            'rarity': 'common',
            'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
        },
        
        # 부시들 (기존)
        {
            'item_type': 'bush',
            'item_name': '연한 초록 부시',
            'item_description': '연한 초록색 부시',
            'item_image': 'assets/images/garden/bushes/bush/light_green/horizontal_regular.png',
            'price': 6,
            'rarity': 'common',
            'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
        },
        {
            'item_type': 'bush',
            'item_name': '초록 부시',
            'item_description': '진한 초록색 부시',
            'item_image': 'assets/images/garden/bushes/bush/green/horizontal_regular.png',
            'price': 6,
            'rarity': 'common',
            'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
        },
        {
            'item_type': 'bush',
            'item_name': '이끼 초록 부시',
            'item_description': '이끼색 부시',
            'item_image': 'assets/images/garden/bushes/bush/moss_green/horizontal_regular.png',
            'price': 6,
            'rarity': 'common',
            'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
        },
        {
            'item_type': 'bush',
            'item_name': '어두운 이끼 초록 부시',
            'item_description': '어두운 이끼색 부시',
            'item_image': 'assets/images/garden/bushes/bush/dark_moss_green/horizontal_regular.png',
            'price': 6,
            'rarity': 'common',
            'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
        },
        
        # 다리 (기존)
        {
            'item_type': 'bridge',
            'item_name': '나무 다리',
            'item_description': '자연스러운 나무 다리',
            'item_image': 'assets/images/garden/bridge/bridge_horizontal.png',
            'price': 20,
            'rarity': 'rare',
            'variants': ['horizontal', 'vertical', 'left', 'right', 'top', 'bottom']
        },
        
        # 연못 (기존)
        {
            'item_type': 'pond',
            'item_name': '연못',
            'item_description': '아름다운 연못',
            'item_image': 'assets/images/garden/pond/pond/Direction=🔄 Center.png',
            'price': 25,
            'rarity': 'rare',
            'variants': ['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right', 'left', 'right', 'top', 'bottom']
        },
        
        # 연못 테두리 (새로 추가)
        {
            'item_type': 'pond_border',
            'item_name': '초록 연못 테두리',
            'item_description': '초록색 연못 테두리',
            'item_image': 'assets/images/garden/pond/pond_borders/green/Border Option=🌳 Bush, Color=Green, Direction=⬅️ Left.png',
            'price': 12,
            'rarity': 'common',
            'variants': ['left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
        },
        {
            'item_type': 'pond_border',
            'item_name': '연한 초록 연못 테두리',
            'item_description': '연한 초록색 연못 테두리',
            'item_image': 'assets/images/garden/pond/pond_borders/light_green/Border Option=🌳 Bush, Color=Light Green, Direction=⬅️ Left.png',
            'price': 12,
            'rarity': 'common',
            'variants': ['left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
        },
        {
            'item_type': 'pond_border',
            'item_name': '회색 연못 테두리',
            'item_description': '회색 연못 테두리',
            'item_image': 'assets/images/garden/pond/pond_borders/grey/Border Option=🌳 Bush, Color=Grey, Direction=⬅️ Left.png',
            'price': 12,
            'rarity': 'common',
            'variants': ['left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
        },
        {
            'item_type': 'pond_border',
            'item_name': '어두운 회색 연못 테두리',
            'item_description': '어두운 회색 연못 테두리',
            'item_image': 'assets/images/garden/pond/pond_borders/dark_grey/Border Option=🌳 Bush, Color=Dark Grey, Direction=⬅️ Left.png',
            'price': 12,
            'rarity': 'common',
            'variants': ['left', 'right', 'top', 'bottom', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
        },
        
        # 물고기들 (기존)
        {
            'item_type': 'fish',
            'item_name': '빨간 물고기',
            'item_description': '활발한 빨간 물고기',
            'item_image': 'assets/images/garden/fishes/red.png',
            'price': 12,
            'rarity': 'common'
        },
        {
            'item_type': 'fish',
            'item_name': '주황 물고기',
            'item_description': '귀여운 주황 물고기',
            'item_image': 'assets/images/garden/fishes/orange.png',
            'price': 12,
            'rarity': 'common'
        },
        
        # 연꽃들 (새로 추가)
        {
            'item_type': 'lotus',
            'item_name': '연한 초록 연꽃',
            'item_description': '연한 초록색 연꽃',
            'item_image': 'assets/images/garden/lotus/light_green.png',
            'price': 15,
            'rarity': 'rare',
            'variants': ['light_green', 'green', 'moss_green', 'dark_moss_green']
        },
        {
            'item_type': 'lotus',
            'item_name': '초록 연꽃',
            'item_description': '초록색 연꽃',
            'item_image': 'assets/images/garden/lotus/green.png',
            'price': 15,
            'rarity': 'rare',
            'variants': ['light_green', 'green', 'moss_green', 'dark_moss_green']
        },
        {
            'item_type': 'lotus',
            'item_name': '이끼 초록 연꽃',
            'item_description': '이끼색 연꽃',
            'item_image': 'assets/images/garden/lotus/moss_green.png',
            'price': 15,
            'rarity': 'rare',
            'variants': ['light_green', 'green', 'moss_green', 'dark_moss_green']
        },
        {
            'item_type': 'lotus',
            'item_name': '어두운 이끼 초록 연꽃',
            'item_description': '어두운 이끼색 연꽃',
            'item_image': 'assets/images/garden/lotus/dark_moss_green.png',
            'price': 15,
            'rarity': 'rare',
            'variants': ['light_green', 'green', 'moss_green', 'dark_moss_green']
        },
        
        # 채소들 (기존 + 패들 추가)
        {
            'item_type': 'veggie',
            'item_name': '토마토',
            'item_description': '신선한 토마토',
            'item_image': 'assets/images/garden/veggie/single/Type=Tomato.png',
            'price': 8,
            'rarity': 'common',
            'variants': ['single', 'paddle']
        },
        {
            'item_type': 'veggie',
            'item_name': '딸기',
            'item_description': '달콤한 딸기',
            'item_image': 'assets/images/garden/veggie/single/Type=Strawberry.png',
            'price': 8,
            'rarity': 'common',
            'variants': ['single', 'paddle']
        },
        {
            'item_type': 'veggie',
            'item_name': '당근',
            'item_description': '영양만점 당근',
            'item_image': 'assets/images/garden/veggie/single/Type=Carrot.png',
            'price': 8,
            'rarity': 'common',
            'variants': ['single', 'paddle']
        },
        {
            'item_type': 'veggie',
            'item_name': '양파',
            'item_description': '향긋한 양파',
            'item_image': 'assets/images/garden/veggie/single/Type=Onion.png',
            'price': 8,
            'rarity': 'common',
            'variants': ['single', 'paddle']
        },
        {
            'item_type': 'veggie',
            'item_name': '마늘',
            'item_description': '강한 마늘',
            'item_image': 'assets/images/garden/veggie/single/Type=Garlic.png',
            'price': 8,
            'rarity': 'common',
            'variants': ['single', 'paddle']
        },
        {
            'item_type': 'veggie',
            'item_name': '오이',
            'item_description': '시원한 오이',
            'item_image': 'assets/images/garden/veggie/single/Type=Cucumber.png',
            'price': 8,
            'rarity': 'common',
            'variants': ['single', 'paddle']
        },
        {
            'item_type': 'veggie',
            'item_name': '체리 토마토',
            'item_description': '작고 귀여운 체리 토마토',
            'item_image': 'assets/images/garden/veggie/single/Type=Cherry Tomatoes.png',
            'price': 8,
            'rarity': 'common',
            'variants': ['single', 'paddle']
        },
        {
            'item_type': 'veggie',
            'item_name': '무',
            'item_description': '싱싱한 무',
            'item_image': 'assets/images/garden/veggie/single/Type=Radish.png',
            'price': 8,
            'rarity': 'common',
            'variants': ['single', 'paddle']
        },
        
        # 배경들 (기존)
        {
            'item_type': 'background',
            'item_name': '잔디 배경',
            'item_description': '자연스러운 잔디 배경',
            'item_image': 'assets/images/garden/backgrounds/Options=🌱 Grass.png',
            'price': 20,
            'rarity': 'common'
        },
        {
            'item_type': 'background',
            'item_name': '모래 배경',
            'item_description': '따뜻한 모래 배경',
            'item_image': 'assets/images/garden/backgrounds/Options=🏝️ Sand.png',
            'price': 20,
            'rarity': 'common'
        },
        {
            'item_type': 'background',
            'item_name': '흙 배경',
            'item_description': '자연스러운 흙 배경',
            'item_image': 'assets/images/garden/backgrounds/Options=🪱 Soil.png',
            'price': 20,
            'rarity': 'common'
        },
    ]
    
    # 아이템들을 데이터베이스에 추가
    for item_data in shop_items:
        # 기존 아이템이 있는지 확인
        existing_item = db.query(GardenItemTemplate).filter(
            GardenItemTemplate.item_name == item_data['item_name']
        ).first()
        
        if not existing_item:
            template = GardenItemTemplate(
                item_type=item_data['item_type'],
                item_name=item_data['item_name'],
                item_description=item_data['item_description'],
                item_image=item_data['item_image'],
                price=item_data['price'],
                rarity=item_data['rarity'],
                is_available=True
            )
            db.add(template)
            print(f"추가됨: {item_data['item_name']}")
        else:
            print(f"이미 존재함: {item_data['item_name']}")
    
    db.commit()
    print(f"\n총 {len(shop_items)}개의 아이템이 처리되었습니다.")
    db.close()

if __name__ == "__main__":
    add_all_garden_items() 