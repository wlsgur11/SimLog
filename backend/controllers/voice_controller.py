from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from services.ai_analysis_service import AIAnalysisService
from services.user_service import get_current_user
from models.user import User
import tempfile
import os

router = APIRouter(prefix="/voice", tags=["voice"])

@router.post("/speech-to-text")
async def speech_to_text(
    audio_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """음성 파일을 텍스트로 변환 (NAVER CLOVA Speech Recognition)"""
    
    # 파일 형식 검증
    if not audio_file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400, 
            detail="지원하는 오디오 형식: WAV, MP3, M4A, FLAC"
        )
    
    try:
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # CLOVA Speech Recognition으로 음성 인식
        text = AIAnalysisService.speech_to_text_with_clova(temp_file_path)
        
        # 임시 파일 삭제
        os.unlink(temp_file_path)
        
        if text:
            return {
                "success": True,
                "text": text,
                "message": "음성이 성공적으로 텍스트로 변환되었습니다."
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="음성 인식에 실패했습니다. 오디오 파일을 확인해주세요."
            )
            
    except Exception as e:
        # 임시 파일 정리
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        
        raise HTTPException(
            status_code=500,
            detail=f"음성 인식 처리 중 오류가 발생했습니다: {str(e)}"
        )

@router.post("/voice-to-emotion")
async def voice_to_emotion(
    audio_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """음성 파일을 텍스트로 변환 후 감정 분석"""
    
    try:
        # 1단계: 음성을 텍스트로 변환
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        text = AIAnalysisService.speech_to_text_with_clova(temp_file_path)
        os.unlink(temp_file_path)
        
        if not text:
            raise HTTPException(
                status_code=500,
                detail="음성 인식에 실패했습니다."
            )
        
        # 2단계: 텍스트를 감정 분석
        emotion_analysis = AIAnalysisService.analyze_emotion_with_ai(text)
        
        # 3단계: 요약 생성
        summary = AIAnalysisService.generate_summary_with_ai(text)
        
        return {
            "success": True,
            "original_text": text,
            "emotion_analysis": emotion_analysis,
            "summary": summary,
            "message": "음성 분석이 완료되었습니다."
        }
        
    except Exception as e:
        # 임시 파일 정리
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        
        raise HTTPException(
            status_code=500,
            detail=f"음성 분석 중 오류가 발생했습니다: {str(e)}"
        ) 