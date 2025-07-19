from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime

from database import get_db
from services.record_service import RecordService
from services.user_service import get_current_user
from models.user import User

router = APIRouter(prefix="/records", tags=["records"])

# Pydantic 모델들
class RecordCreate(BaseModel):
    content: str
    sleep_score: Optional[int] = None
    stress_score: Optional[int] = None
    share_with_counselor: bool = False

class RecordUpdate(BaseModel):
    content: Optional[str] = None
    sleep_score: Optional[int] = None
    stress_score: Optional[int] = None
    share_with_counselor: Optional[bool] = None

class RecordResponse(BaseModel):
    id: int
    content: str
    sleep_score: Optional[int]
    stress_score: Optional[int]
    ai_keywords: List[str]
    ai_summary: str
    emotion_analysis: Dict
    share_with_counselor: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# API 엔드포인트들
@router.post("/", response_model=RecordResponse)
def create_record(
    record_data: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """감정 기록 생성 (하루에 한 번만 가능)"""
    try:
        record = RecordService.create_record(
            db=db,
            user_id=current_user.id,
            content=record_data.content,
            sleep_score=record_data.sleep_score,
            stress_score=record_data.stress_score,
            share_with_counselor=record_data.share_with_counselor
        )
        return record
    except ValueError as e:
        # 하루에 한 번 제한 관련 에러
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"감정 기록 생성 실패: {str(e)}")

@router.get("/", response_model=List[RecordResponse])
def get_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """사용자의 감정 기록 목록 조회 (최신순)"""
    try:
        records = RecordService.get_user_records(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit
        )
        return records
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"감정 기록 조회 실패: {str(e)}")

@router.get("/period/{days}", response_model=List[RecordResponse])
def get_records_by_period(
    days: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """사용자의 특정 기간 감정 기록 조회 (최신순)"""
    try:
        if days <= 0 or days > 365:
            raise HTTPException(status_code=400, detail="조회 기간은 1일~365일 사이여야 합니다.")
        
        records = RecordService.get_user_records_by_period(
            db=db,
            user_id=current_user.id,
            days=days
        )
        return records
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"기간별 기록 조회 실패: {str(e)}")

@router.get("/count")
def get_records_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """사용자의 총 감정 기록 수 조회"""
    try:
        count = RecordService.get_user_records_count(
            db=db,
            user_id=current_user.id
        )
        return {
            "user_id": current_user.id,
            "total_records": count,
            "message": f"총 {count}개의 감정 기록이 있습니다."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"기록 수 조회 실패: {str(e)}")

@router.get("/{record_id}", response_model=RecordResponse)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """특정 감정 기록 조회"""
    try:
        record = RecordService.get_record(
            db=db,
            record_id=record_id,
            user_id=current_user.id
        )
        if not record:
            raise HTTPException(status_code=404, detail="감정 기록을 찾을 수 없습니다.")
        return record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"감정 기록 조회 실패: {str(e)}")

@router.get("/today/record", response_model=RecordResponse)
def get_today_record(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """오늘 작성한 감정 기록 조회"""
    try:
        record = RecordService.get_today_record(
            db=db,
            user_id=current_user.id
        )
        if not record:
            raise HTTPException(status_code=404, detail="오늘 작성한 감정 기록이 없습니다.")
        return record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"오늘 기록 조회 실패: {str(e)}")

@router.get("/today/status")
def get_today_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """오늘 감정 기록 작성 상태 조회"""
    try:
        record = RecordService.get_today_record(
            db=db,
            user_id=current_user.id
        )
        
        if record:
            return {
                "has_record": True,
                "message": "오늘 감정 기록을 작성했습니다.",
                "record_id": record.id,
                "created_at": record.created_at
            }
        else:
            return {
                "has_record": False,
                "message": "오늘 아직 감정 기록을 작성하지 않았습니다.",
                "can_write": True
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"오늘 상태 조회 실패: {str(e)}")

@router.put("/{record_id}", response_model=RecordResponse)
def update_record(
    record_id: int,
    record_data: RecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """감정 기록 수정"""
    try:
        record = RecordService.update_record(
            db=db,
            record_id=record_id,
            user_id=current_user.id,
            content=record_data.content,
            sleep_score=record_data.sleep_score,
            stress_score=record_data.stress_score,
            share_with_counselor=record_data.share_with_counselor
        )
        if not record:
            raise HTTPException(status_code=404, detail="감정 기록을 찾을 수 없습니다.")
        return record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"감정 기록 수정 실패: {str(e)}")

@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """감정 기록 삭제"""
    try:
        success = RecordService.delete_record(
            db=db,
            record_id=record_id,
            user_id=current_user.id
        )
        if not success:
            raise HTTPException(status_code=404, detail="감정 기록을 찾을 수 없습니다.")
        return {"message": "감정 기록이 삭제되었습니다."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"감정 기록 삭제 실패: {str(e)}")

@router.get("/statistics/{days}")
def get_emotion_statistics(
    days: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """감정 통계 조회 (일주일: 7, 이주일: 14, 한달: 30)"""
    try:
        if days not in [7, 14, 30]:
            raise HTTPException(status_code=400, detail="지원하는 기간: 7일, 14일, 30일")
        
        statistics = RecordService.get_emotion_statistics(
            db=db,
            user_id=current_user.id,
            days=days
        )
        return statistics
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"감정 통계 조회 실패: {str(e)}") 