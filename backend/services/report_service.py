from sqlalchemy.orm import Session
from typing import Optional, Dict, List
from datetime import datetime, timedelta, timezone
import secrets
import hashlib

from models.weekly_summary import WeeklySummaryCache
from models.shared_report import SharedReport
from models.user_consent import UserConsent


class ReportService:
    @staticmethod
    def _to_aware_utc(dt: datetime) -> datetime:
        if dt is None:
            return datetime.now(timezone.utc)
        if dt.tzinfo is None:
            # DB에서 naive로 돌아온 경우 UTC 기준으로 간주
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    @staticmethod
    def _generate_token() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def _digest_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @staticmethod
    def get_consent(db: Session, user_id: int) -> bool:
        consent = db.query(UserConsent).filter(UserConsent.user_id == user_id).first()
        return bool(consent and consent.consented)

    @staticmethod
    def set_consent(db: Session, user_id: int, consented: bool) -> Dict:
        consent = db.query(UserConsent).filter(UserConsent.user_id == user_id).first()
        now = datetime.now(timezone.utc)
        if not consent:
            consent = UserConsent(user_id=user_id)
            db.add(consent)
        consent.consented = consented
        if consented:
            consent.consented_at = now
            consent.revoked_at = None
        else:
            consent.revoked_at = now
        db.commit()
        db.refresh(consent)
        return {
            "user_id": user_id,
            "consented": consent.consented,
            "consented_at": consent.consented_at,
            "revoked_at": consent.revoked_at,
        }

    @staticmethod
    def create_weekly_share(db: Session, user_id: int, period_days: int = 7, expires_in_days: int = 7) -> Dict:
        # 동의 확인
        if not ReportService.get_consent(db, user_id):
            raise ValueError("사용자가 공유에 동의하지 않았습니다.")

        cache: Optional[WeeklySummaryCache] = db.query(WeeklySummaryCache).filter(
            WeeklySummaryCache.user_id == user_id,
            WeeklySummaryCache.period_days == period_days
        ).first()

        if not cache or not cache.items:
            raise ValueError("최근 요약 데이터가 없습니다.")

        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=expires_in_days)

        snapshot = {
            "period": cache.period_days,
            "items": cache.items,
            "one_line_summary": cache.one_line_summary or "",
            "negative_ratio": cache.negative_ratio or 0.0,
            "generated_at": now.isoformat(),
        }

        token = ReportService._generate_token()
        token_digest = ReportService._digest_token(token)

        share = SharedReport(
            user_id=user_id,
            token_digest=token_digest,
            snapshot=snapshot,
            expires_at=expires_at,
            revoked=False,
        )
        db.add(share)
        db.commit()
        db.refresh(share)

        return {
            "token": token,
            "expires_at": expires_at,
        }

    @staticmethod
    def get_shared_report(db: Session, token: str) -> Dict:
        token_digest = ReportService._digest_token(token)
        share = db.query(SharedReport).filter(SharedReport.token_digest == token_digest).first()
        if not share or share.revoked:
            raise ValueError("유효하지 않은 공유 링크입니다.")
        now = datetime.now(timezone.utc)
        # naive/aware 혼용 대비하여 UTC aware로 변환 후 비교
        expires_at = ReportService._to_aware_utc(share.expires_at)
        now_aware = ReportService._to_aware_utc(now)
        if expires_at < now_aware:
            raise ValueError("만료된 공유 링크입니다.")
        return share.snapshot

    @staticmethod
    def revoke_shared_report(db: Session, user_id: int, token: str) -> bool:
        token_digest = ReportService._digest_token(token)
        share = db.query(SharedReport).filter(
            SharedReport.token_digest == token_digest,
            SharedReport.user_id == user_id
        ).first()
        if not share:
            return False
        share.revoked = True
        db.commit()
        return True

    @staticmethod
    def list_active_shares(db: Session, user_id: int) -> List[Dict]:
        now = datetime.now(timezone.utc)
        shares = db.query(SharedReport).filter(
            SharedReport.user_id == user_id,
            SharedReport.revoked == False,
            SharedReport.expires_at >= now
        ).all()
        return [
            {
                "created_at": ReportService._to_aware_utc(s.created_at),
                "expires_at": ReportService._to_aware_utc(s.expires_at),
            }
            for s in shares
        ]

