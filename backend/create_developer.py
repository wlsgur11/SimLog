"""
개발자 계정 생성 스크립트
"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models.user import User
from models.record import Record
from passlib.context import CryptContext

# 환경 변수 로딩
load_dotenv(dotenv_path=".env")

# 비밀번호 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_developer_account():
    """개발자 계정 생성"""
    db = SessionLocal()
    
    try:
        # 개발자 계정 정보
        developer_email = "developer@simlog.com"
        developer_nickname = "개발자"
        developer_password = "dev1234!"
        
        # 기존 개발자 계정 확인
        existing_user = db.query(User).filter(
            (User.email == developer_email) | (User.nickname == developer_nickname)
        ).first()
        
        if existing_user:
            print(f"개발자 계정이 이미 존재합니다: {existing_user.nickname}")
            if not existing_user.is_developer:
                # 기존 계정을 개발자 모드로 변경
                existing_user.is_developer = True
                db.commit()
                print("기존 계정을 개발자 모드로 변경했습니다.")
            return existing_user
        
        # 새 개발자 계정 생성
        hashed_password = pwd_context.hash(developer_password)
        
        developer_user = User(
            email=developer_email,
            password=hashed_password,
            nickname=developer_nickname,
            is_developer=True
        )
        
        db.add(developer_user)
        db.commit()
        db.refresh(developer_user)
        
        print("개발자 계정이 성공적으로 생성되었습니다!")
        print(f"이메일: {developer_email}")
        print(f"비밀번호: {developer_password}")
        print(f"닉네임: {developer_nickname}")
        print("이제 하루 제한 없이 감정 기록을 생성할 수 있습니다!")
        
        return developer_user
        
    except Exception as e:
        print(f"개발자 계정 생성 중 오류 발생: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def list_developer_accounts():
    """개발자 계정 목록 조회"""
    db = SessionLocal()
    
    try:
        developers = db.query(User).filter(User.is_developer == True).all()
        
        if not developers:
            print("개발자 계정이 없습니다.")
            return
        
        print("개발자 계정 목록:")
        for dev in developers:
            print(f"- ID: {dev.id}, 이메일: {dev.email}, 닉네임: {dev.nickname}")
            
    except Exception as e:
        print(f"개발자 계정 목록 조회 중 오류 발생: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_developer_accounts()
    else:
        create_developer_account() 