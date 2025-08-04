from sqlalchemy.orm import Session
from database import engine, get_db
from models.garden_item import GardenItemTemplate, GardenItem
from datetime import datetime

def clear_garden_items():
    print("기존의 모든 정원 아이템들을 삭제합니다...")
    
    # 데이터베이스 세션 생성
    db = Session(engine)
    
    try:
        # 모든 템플릿 아이템 삭제
        deleted_templates = db.query(GardenItemTemplate).delete()
        print(f"✓ {deleted_templates}개의 템플릿 아이템 삭제 완료")
        
        # 모든 사용자 아이템 삭제
        deleted_items = db.query(GardenItem).delete()
        print(f"✓ {deleted_items}개의 사용자 아이템 삭제 완료")
        
        db.commit()
        print("✅ 모든 정원 아이템 삭제가 완료되었습니다!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    clear_garden_items() 