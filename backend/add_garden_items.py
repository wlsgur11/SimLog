from sqlalchemy.orm import Session
from database import engine, get_db
from models.garden_item import GardenItemTemplate
from datetime import datetime

def add_garden_items():
    print("새로운 정원 아이템들을 추가합니다...")
    
    # 데이터베이스 세션 생성
    db = Session(engine)
    
    try:
        # 색상별 울타리 아이템들
        fence_items = [
            # Light Green 울타리
            {
                'item_type': 'decoration',
                'item_name': '연한 초록 울타리 (가로)',
                'item_description': '연한 초록색 가로 울타리',
                'item_image': 'assets/images/garden/colors/light_green/horizontal_regular.png',
                'price': 15,
                'rarity': 'common'
            },
            {
                'item_type': 'decoration',
                'item_name': '연한 초록 울타리 (세로)',
                'item_description': '연한 초록색 세로 울타리',
                'item_image': 'assets/images/garden/colors/light_green/vertical_regular.png',
                'price': 15,
                'rarity': 'common'
            },
            {
                'item_type': 'decoration',
                'item_name': '연한 초록 울타리 (왼쪽)',
                'item_description': '연한 초록색 왼쪽 울타리',
                'item_image': 'assets/images/garden/colors/light_green/left_regular.png',
                'price': 15,
                'rarity': 'common'
            },
            {
                'item_type': 'decoration',
                'item_name': '연한 초록 울타리 (오른쪽)',
                'item_description': '연한 초록색 오른쪽 울타리',
                'item_image': 'assets/images/garden/colors/light_green/right_regular.png',
                'price': 15,
                'rarity': 'common'
            },
            {
                'item_type': 'decoration',
                'item_name': '연한 초록 울타리 (위쪽)',
                'item_description': '연한 초록색 위쪽 울타리',
                'item_image': 'assets/images/garden/colors/light_green/top_regular.png',
                'price': 15,
                'rarity': 'common'
            },
            {
                'item_type': 'decoration',
                'item_name': '연한 초록 울타리 (아래쪽)',
                'item_description': '연한 초록색 아래쪽 울타리',
                'item_image': 'assets/images/garden/colors/light_green/bottom_regular.png',
                'price': 15,
                'rarity': 'common'
            },
            
            # Green 울타리
            {
                'item_type': 'decoration',
                'item_name': '초록 울타리 (가로)',
                'item_description': '초록색 가로 울타리',
                'item_image': 'assets/images/garden/colors/green/horizontal_regular.png',
                'price': 15,
                'rarity': 'common'
            },
            {
                'item_type': 'decoration',
                'item_name': '초록 울타리 (세로)',
                'item_description': '초록색 세로 울타리',
                'item_image': 'assets/images/garden/colors/green/vertical_regular.png',
                'price': 15,
                'rarity': 'common'
            },
            {
                'item_type': 'decoration',
                'item_name': '초록 울타리 (왼쪽)',
                'item_description': '초록색 왼쪽 울타리',
                'item_image': 'assets/images/garden/colors/green/left_regular.png',
                'price': 15,
                'rarity': 'common'
            },
            {
                'item_type': 'decoration',
                'item_name': '초록 울타리 (오른쪽)',
                'item_description': '초록색 오른쪽 울타리',
                'item_image': 'assets/images/garden/colors/green/right_regular.png',
                'price': 15,
                'rarity': 'common'
            },
            {
                'item_type': 'decoration',
                'item_name': '초록 울타리 (위쪽)',
                'item_description': '초록색 위쪽 울타리',
                'item_image': 'assets/images/garden/colors/green/top_regular.png',
                'price': 15,
                'rarity': 'common'
            },
            {
                'item_type': 'decoration',
                'item_name': '초록 울타리 (아래쪽)',
                'item_description': '초록색 아래쪽 울타리',
                'item_image': 'assets/images/garden/colors/green/bottom_regular.png',
                'price': 15,
                'rarity': 'common'
            },
            
            # Dark Moss Green 울타리
            {
                'item_type': 'decoration',
                'item_name': '어두운 이끼 초록 울타리 (가로)',
                'item_description': '어두운 이끼 초록색 가로 울타리',
                'item_image': 'assets/images/garden/colors/dark_moss_green/horizontal_regular.png',
                'price': 20,
                'rarity': 'rare'
            },
            {
                'item_type': 'decoration',
                'item_name': '어두운 이끼 초록 울타리 (세로)',
                'item_description': '어두운 이끼 초록색 세로 울타리',
                'item_image': 'assets/images/garden/colors/dark_moss_green/vertical_regular.png',
                'price': 20,
                'rarity': 'rare'
            },
            {
                'item_type': 'decoration',
                'item_name': '어두운 이끼 초록 울타리 (왼쪽)',
                'item_description': '어두운 이끼 초록색 왼쪽 울타리',
                'item_image': 'assets/images/garden/colors/dark_moss_green/left_regular.png',
                'price': 20,
                'rarity': 'rare'
            },
            {
                'item_type': 'decoration',
                'item_name': '어두운 이끼 초록 울타리 (오른쪽)',
                'item_description': '어두운 이끼 초록색 오른쪽 울타리',
                'item_image': 'assets/images/garden/colors/dark_moss_green/right_regular.png',
                'price': 20,
                'rarity': 'rare'
            },
            {
                'item_type': 'decoration',
                'item_name': '어두운 이끼 초록 울타리 (위쪽)',
                'item_description': '어두운 이끼 초록색 위쪽 울타리',
                'item_image': 'assets/images/garden/colors/dark_moss_green/top_regular.png',
                'price': 20,
                'rarity': 'rare'
            },
            {
                'item_type': 'decoration',
                'item_name': '어두운 이끼 초록 울타리 (아래쪽)',
                'item_description': '어두운 이끼 초록색 아래쪽 울타리',
                'item_image': 'assets/images/garden/colors/dark_moss_green/bottom_regular.png',
                'price': 20,
                'rarity': 'rare'
            },
            
            # Moss Green 울타리
            {
                'item_type': 'decoration',
                'item_name': '이끼 초록 울타리 (가로)',
                'item_description': '이끼 초록색 가로 울타리',
                'item_image': 'assets/images/garden/colors/moss_green/horizontal_regular.png',
                'price': 18,
                'rarity': 'rare'
            },
            {
                'item_type': 'decoration',
                'item_name': '이끼 초록 울타리 (세로)',
                'item_description': '이끼 초록색 세로 울타리',
                'item_image': 'assets/images/garden/colors/moss_green/vertical_regular.png',
                'price': 18,
                'rarity': 'rare'
            },
            {
                'item_type': 'decoration',
                'item_name': '이끼 초록 울타리 (왼쪽)',
                'item_description': '이끼 초록색 왼쪽 울타리',
                'item_image': 'assets/images/garden/colors/moss_green/left_regular.png',
                'price': 18,
                'rarity': 'rare'
            },
            {
                'item_type': 'decoration',
                'item_name': '이끼 초록 울타리 (오른쪽)',
                'item_description': '이끼 초록색 오른쪽 울타리',
                'item_image': 'assets/images/garden/colors/moss_green/right_regular.png',
                'price': 18,
                'rarity': 'rare'
            },
            {
                'item_type': 'decoration',
                'item_name': '이끼 초록 울타리 (위쪽)',
                'item_description': '이끼 초록색 위쪽 울타리',
                'item_image': 'assets/images/garden/colors/moss_green/top_regular.png',
                'price': 18,
                'rarity': 'rare'
            },
            {
                'item_type': 'decoration',
                'item_name': '이끼 초록 울타리 (아래쪽)',
                'item_description': '이끼 초록색 아래쪽 울타리',
                'item_image': 'assets/images/garden/colors/moss_green/bottom_regular.png',
                'price': 18,
                'rarity': 'rare'
            },
        ]
        
        # 기존 아이템 확인 후 추가
        for item_data in fence_items:
            existing = db.query(GardenItemTemplate).filter(
                GardenItemTemplate.item_name == item_data['item_name']
            ).first()
            
            if not existing:
                template = GardenItemTemplate(**item_data)
                db.add(template)
                print(f"✓ 추가됨: {item_data['item_name']}")
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
    add_garden_items() 