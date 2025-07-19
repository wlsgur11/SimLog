from fastapi import APIRouter, Depends
from services.emotion_color_service import EmotionColorService
from services.user_service import get_current_user
from models.user import User

router = APIRouter(prefix="/emotions", tags=["emotions"])

@router.get("/colors")
def get_emotion_colors(current_user: User = Depends(get_current_user)):
    """감정의 바퀴 기반 색상 정보 조회"""
    return {
        "emotion_colors": EmotionColorService.get_emotion_colors(),
        "description": "로버트 플루치크의 감정의 바퀴를 기반으로 한 8가지 기본 감정 색상입니다."
    }

@router.get("/analyze")
def analyze_text_emotion(text: str, current_user: User = Depends(get_current_user)):
    """텍스트 감정 분석 (테스트용)"""
    from services.ai_analysis_service import AIAnalysisService
    analysis = AIAnalysisService.analyze_emotion_with_ai(text)
    return analysis

@router.get("/analyze-ai")
def analyze_text_emotion_ai(text: str, current_user: User = Depends(get_current_user)):
    """텍스트 감정 분석 (AI API만 사용)"""
    from services.ai_analysis_service import AIAnalysisService
    analysis = AIAnalysisService.analyze_emotion_with_gpt4o(text)
    if analysis:
        return AIAnalysisService._convert_ai_result_to_color(analysis)
    else:
        return {"error": "AI API 호출 실패"}

@router.get("/summarize")
def summarize_text(text: str, current_user: User = Depends(get_current_user)):
    """텍스트 요약 (AI API 사용)"""
    from services.ai_analysis_service import AIAnalysisService
    summary = AIAnalysisService.generate_summary_with_ai(text)
    return {
        "original_text": text,
        "summary": summary,
        "ai_used": True
    } 