from fastapi import APIRouter, Depends
from services.emotion_color_service import EmotionColorService
from services.user_service import get_current_user
from models.user import User
import os

router = APIRouter(prefix="/emotions", tags=["emotions"])

@router.get("/colors")
def get_emotion_colors(current_user: User = Depends(get_current_user)):
    """감정의 바퀴 기반 색상 정보 조회"""
    return {
        "emotion_colors": EmotionColorService.get_emotion_colors(),
        "description": "로버트 플루치크의 감정의 바퀴를 기반으로 한 8가지 기본 감정 색상입니다."
    }

@router.get("/debug/ai-status")
def check_ai_status(current_user: User = Depends(get_current_user)):
    """AI API 상태 확인 (디버깅용)"""
    api_key = os.getenv("OPENAI_API_KEY")
    return {
        "api_key_exists": bool(api_key),
        "api_key_preview": api_key[:10] + "..." if api_key else None,
        "message": "AI API 키가 설정되어 있습니다." if api_key else "AI API 키가 설정되지 않았습니다."
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
    import os
    
    # API 키 상태 확인
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"🔍 AI 전용 분석 시작 - API Key 존재: {bool(api_key)}")
    
    try:
        analysis = AIAnalysisService.analyze_emotion_with_gpt4o(text)
        print(f"🔍 AI 분석 결과: {analysis}")
        
        if analysis:
            result = AIAnalysisService._convert_ai_result_to_color(analysis)
            print(f"✅ AI 분석 성공: {result}")
            return result
        else:
            print("❌ AI 분석 실패: None 반환")
            return {"error": "AI API 호출 실패", "details": "분석 결과가 None입니다"}
            
    except Exception as e:
        print(f"❌ AI 분석 중 예외 발생: {str(e)}")
        return {"error": "AI API 호출 실패", "details": str(e)}

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