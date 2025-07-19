from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    password = Column(String(255), nullable=True)
    nickname = Column(String(50), unique=True, index=True)
    social_type = Column(String(20), nullable=True)
    social_id = Column(String(100), nullable=True)
    is_developer = Column(Boolean, default=False)  # 개발자 모드 플래그
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계 설정
    records = relationship("Record", back_populates="user") 