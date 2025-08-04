from sqlalchemy.orm import Session
from database import engine, get_db
from models.user import User
from models.garden_item import GardenItem, GardenItemTemplate
from datetime import datetime
from sqlalchemy import text

def migrate_garden_system():
    """정원 시스템 마이그레이션"""
    
    # 먼저 데이터베이스 스키마 업데이트
    print("데이터베이스 스키마를 업데이트합니다...")
    from models import User, Record, GardenItem, GardenItemTemplate
    from database import Base
    
    # 새로운 테이블들 생성
    Base.metadata.create_all(bind=engine)
    print("새 테이블 생성 완료!")
    
    # 기존 users 테이블에 새로운 컬럼들 추가
    print("기존 users 테이블에 새로운 컬럼들을 추가합니다...")
    with engine.connect() as conn:
        try:
            # seeds 컬럼 추가
            conn.execute(text("ALTER TABLE users ADD COLUMN seeds INTEGER DEFAULT 10"))
            print("seeds 컬럼 추가 완료")
        except Exception as e:
            print(f"seeds 컬럼이 이미 존재하거나 오류: {e}")
        
        try:
            # last_attendance_date 컬럼 추가
            conn.execute(text("ALTER TABLE users ADD COLUMN last_attendance_date DATETIME"))
            print("last_attendance_date 컬럼 추가 완료")
        except Exception as e:
            print(f"last_attendance_date 컬럼이 이미 존재하거나 오류: {e}")
        
        try:
            # attendance_streak 컬럼 추가
            conn.execute(text("ALTER TABLE users ADD COLUMN attendance_streak INTEGER DEFAULT 0"))
            print("attendance_streak 컬럼 추가 완료")
        except Exception as e:
            print(f"attendance_streak 컬럼이 이미 존재하거나 오류: {e}")
        
        conn.commit()
    
    print("스키마 업데이트 완료!")
    
    # 새로운 데이터베이스 세션 생성 (컬럼 추가 후)
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 기존 사용자들에게 기본 씨앗 지급
        print("기존 사용자들에게 기본 씨앗을 지급합니다...")
        
        # SQL을 직접 실행하여 사용자들을 업데이트
        with engine.connect() as conn:
            # 모든 사용자 조회
            result = conn.execute(text("SELECT id FROM users"))
            user_ids = [row[0] for row in result]
            
            # 각 사용자에게 기본 씨앗 지급
            for user_id in user_ids:
                conn.execute(
                    text("UPDATE users SET seeds = 10, attendance_streak = 0 WHERE id = :user_id"),
                    {"user_id": user_id}
                )
                print(f"사용자 {user_id}에게 기본 씨앗 지급 완료")
            
            conn.commit()
        
        # 기본 상점 아이템 템플릿 생성
        print("기본 상점 아이템을 생성합니다...")
        default_items = [
            {
                'item_type': 'flower',
                'item_name': '기본 꽃',
                'item_description': '정원을 시작할 수 있는 기본 꽃입니다.',
                'item_image': None,
                'price': 5,
                'rarity': 'common'
            },
            {
                'item_type': 'flower',
                'item_name': '장미',
                'item_description': '아름다운 빨간 장미입니다.',
                'item_image': None,
                'price': 15,
                'rarity': 'rare'
            },
            {
                'item_type': 'flower',
                'item_name': '해바라기',
                'item_description': '밝고 긍정적인 해바라기입니다.',
                'item_image': None,
                'price': 20,
                'rarity': 'rare'
            },
            {
                'item_type': 'pot',
                'item_name': '기본 화분',
                'item_description': '꽃을 심을 수 있는 기본 화분입니다.',
                'item_image': None,
                'price': 10,
                'rarity': 'common'
            },
            {
                'item_type': 'pot',
                'item_name': '예쁜 화분',
                'item_description': '꽃을 더욱 아름답게 보여주는 화분입니다.',
                'item_image': None,
                'price': 25,
                'rarity': 'rare'
            },
            {
                'item_type': 'decoration',
                'item_name': '나비 장식',
                'item_description': '정원에 생동감을 더해주는 나비 장식입니다.',
                'item_image': None,
                'price': 30,
                'rarity': 'epic'
            },
            {
                'item_type': 'decoration',
                'item_name': '분수대',
                'item_description': '정원을 더욱 특별하게 만들어주는 분수대입니다.',
                'item_image': None,
                'price': 50,
                'rarity': 'legendary'
            },
            {
                'item_type': 'flower',
                'item_name': '라벤더',
                'item_description': '차분하고 평화로운 라벤더입니다.',
                'item_image': None,
                'price': 35,
                'rarity': 'epic'
            },
            {
                'item_type': 'flower',
                'item_name': '튤립',
                'item_description': '우아하고 고급스러운 튤립입니다.',
                'item_image': None,
                'price': 40,
                'rarity': 'epic'
            },
            {
                'item_type': 'decoration',
                'item_name': '벤치',
                'item_description': '정원에서 휴식을 취할 수 있는 벤치입니다.',
                'item_image': None,
                'price': 45,
                'rarity': 'epic'
            }
        ]
        
        # 기존 템플릿이 있는지 확인하고 없으면 추가
        for item_data in default_items:
            existing = db.query(GardenItemTemplate).filter(
                GardenItemTemplate.item_name == item_data['item_name']
            ).first()
            
            if not existing:
                template = GardenItemTemplate(**item_data)
                db.add(template)
                print(f"아이템 추가: {item_data['item_name']}")
        
        db.commit()
        print("정원 시스템 마이그레이션이 완료되었습니다!")
        
    except Exception as e:
        db.rollback()
        print(f"마이그레이션 중 오류 발생: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    migrate_garden_system() 