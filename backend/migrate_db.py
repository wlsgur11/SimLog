"""
데이터베이스 마이그레이션 스크립트
기존 테이블을 삭제하고 새로운 스키마로 재생성합니다.
"""
from sqlalchemy import text
from database import engine, Base
from models.user import User
from models.record import Record

def migrate_database():
    """데이터베이스 마이그레이션 실행"""
    print("🔄 데이터베이스 마이그레이션을 시작합니다...")
    
    try:
        # 기존 테이블 삭제 (순서 주의: 외래키가 있는 테이블부터)
        print("📋 기존 테이블 삭제 중...")
        
        with engine.connect() as conn:
            # 외래키 제약 조건 비활성화
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # 테이블 삭제
            conn.execute(text("DROP TABLE IF EXISTS records"))
            conn.execute(text("DROP TABLE IF EXISTS users"))
            
            # 외래키 제약 조건 활성화
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            
            conn.commit()
        
        print("✅ 기존 테이블 삭제 완료")
        
        # 새로운 스키마로 테이블 생성
        print("📋 새로운 테이블 생성 중...")
        Base.metadata.create_all(bind=engine)
        print("✅ 새로운 테이블 생성 완료")
        
        print("🎉 데이터베이스 마이그레이션이 완료되었습니다!")
        print("\n📊 생성된 테이블:")
        print("- users (사용자 정보 - is_developer 컬럼 포함)")
        print("- records (감정 기록 - emotion_analysis 컬럼 포함)")
        print("\n🔧 개발자 계정을 생성하려면 다음 명령어를 실행하세요:")
        print("python create_developer.py")
        
    except Exception as e:
        print(f"❌ 마이그레이션 실패: {str(e)}")
        raise

if __name__ == "__main__":
    migrate_database() 