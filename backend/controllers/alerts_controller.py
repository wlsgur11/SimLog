from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from database import get_db
from services.user_service import get_current_user
from models.user import User
from models.weekly_summary import WeeklySummaryCache
from models.alert_state import UserAlertState
from datetime import datetime, timedelta, timezone


router = APIRouter(prefix="/alerts", tags=["alerts"])


NEGATIVE_EMOTIONS = {"우울", "슬픔", "분노", "혐오", "두려움", "불안", "짜증", "화남"}


@router.get("/check")
def check_negative_alert(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # 7일 억제 로직: 최근 7일 이내 마음체크 완료 시 표시하지 않음
        state = db.query(UserAlertState).filter(UserAlertState.user_id == current_user.id).first()
        if state and state.last_mind_check_at:
            now = datetime.now(timezone.utc)
            last = state.last_mind_check_at
            if last.tzinfo is None:
                last = last.replace(tzinfo=timezone.utc)
            if now - last < timedelta(days=7):
                return {"should_alert": False, "suppressed": True}

        cache = db.query(WeeklySummaryCache).filter(
            WeeklySummaryCache.user_id == current_user.id,
            WeeklySummaryCache.period_days == 7
        ).first()
        if not cache or not cache.items:
            return {"should_alert": False}

        items = cache.items or []
        days_negative = sum(1 for it in items if it.get("primary_emotion") in NEGATIVE_EMOTIONS)
        negative_ratio = (days_negative / len(items)) if items else 0.0

        # 기준: 최근 7일 중 5일 이상 부정 or 부정 비율 >= 0.6
        should_alert = (len(items) >= 7 and days_negative >= 5) or negative_ratio >= 0.6

        result = {
            "should_alert": should_alert,
            "period": 7,
            "negative_ratio": round(negative_ratio, 3),
            "days_negative": days_negative,
            "message": "최근 오래도록 힘든 감정이 이어졌어요. 잠깐 숨 고르며 마음을 돌보는 시간이 필요할지 몰라요.",
            "form_url": "https://forms.gle/RM8vijEWkqgPo1de9",
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"알림 검사 실패: {str(e)}")


@router.post("/ack")
def acknowledge_alert(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """사용자가 모달에서 '마음체크' 실행/동의 시 7일 억제를 위한 확인 API."""
    try:
        state = db.query(UserAlertState).filter(UserAlertState.user_id == current_user.id).first()
        now = datetime.now(timezone.utc)
        if not state:
            state = UserAlertState(user_id=current_user.id, last_mind_check_at=now)
            db.add(state)
        else:
            state.last_mind_check_at = now
        db.commit()
        return {"acknowledged_at": now}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"확인 처리 실패: {str(e)}")

