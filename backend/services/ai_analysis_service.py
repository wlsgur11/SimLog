"""
통합 AI 분석 서비스
- 텍스트 요약: GPT-4o mini
- 감정 분류: GPT-4o mini
- 음성 인식: NAVER CLOVA Speech Recognition (CSR)
"""
import os
import json
import base64
from typing import Dict, Optional
import requests
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로딩
load_dotenv(dotenv_path=".env")

class AIAnalysisService:
    """통합 AI 분석 서비스"""
    
    @staticmethod
    def analyze_emotion_with_gpt4o(content: str) -> Optional[Dict]:
        """GPT-4o mini를 사용한 감정 분석"""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            print(f"OpenAI API Key 확인: {api_key[:10] if api_key else 'None'}...")
            if not api_key:
                print("OpenAI API 키가 설정되지 않았습니다.")
                return None
            
            client = OpenAI(api_key=api_key)
            
            prompt = f"""
            다음 텍스트의 감정을 로버트 플루치크의 감정의 바퀴 8가지 중에서 분석해주세요:
            감정: 기쁨, 신뢰, 두려움, 놀람, 슬픔, 혐오, 분노, 기대
            
            텍스트: {content}
            
            반드시 다음 JSON 형태로만 응답해주세요. 다른 텍스트는 포함하지 마세요:
            {{
                "primary_emotion": "감정명",
                "intensity": 1-10 사이의 감정 강도 (1: 매우 약함, 10: 매우 강함),
                "confidence": 0.0-1.0 사이의 분석 확신도 (0.0: 매우 불확실, 1.0: 매우 확실),
                "reasoning": "분석 근거",
                "color_name": "이 감정을 나타내는 색상의 이름 (예: 선명한 빨강, 밝은 노랑, 깊은 파랑 등)"
            }}
            """
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            print(f"OpenAI 응답: {content}")
            
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                print(f"JSON 파싱 오류: {e}")
                print(f"응답 내용: {content}")
                return None
            
        except Exception as e:
            print(f"GPT-4o mini 감정 분석 오류: {str(e)}")
            return None
    
    @staticmethod
    def generate_summary_with_gpt4o(content: str) -> Optional[str]:
        """GPT-4o mini를 사용한 텍스트 요약"""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                return None
            
            client = OpenAI(api_key=api_key)
            
            prompt = f"""
            다음 감정 기록을 한 줄로 요약해주세요. 
            감정의 핵심과 주요 내용을 간결하게 표현해주세요.
            
            텍스트: {content}
            
            요약:
            """
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"GPT-4o mini 요약 생성 오류: {str(e)}")
            return None
    
    @staticmethod
    def speech_to_text_with_clova(audio_file_path: str) -> Optional[str]:
        """NAVER CLOVA Speech Recognition을 사용한 음성 인식"""
        try:
            # CLOVA API 설정
            api_url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt"
            client_id = os.getenv("CLOVA_CLIENT_ID")
            client_secret = os.getenv("CLOVA_CLIENT_SECRET")
            
            if not client_id or not client_secret:
                print("CLOVA API 키가 설정되지 않았습니다.")
                return None
            
            headers = {
                "X-OCR-SECRET": client_secret,
                "Content-Type": "application/octet-stream"
            }
            
            # 오디오 파일 읽기
            with open(audio_file_path, "rb") as audio_file:
                audio_data = audio_file.read()
            
            # API 호출
            response = requests.post(
                api_url,
                headers=headers,
                data=audio_data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("text", "")
            
            return None
            
        except Exception as e:
            print(f"CLOVA 음성 인식 오류: {str(e)}")
            return None
    
    @staticmethod
    def analyze_emotion_fallback(content: str) -> Dict:
        """AI API 실패 시 기본 키워드 분석 사용"""
        from services.emotion_color_service import EmotionColorService
        return EmotionColorService.analyze_emotion_from_text(content)
    
    @staticmethod
    def generate_summary_fallback(content: str) -> str:
        """AI API 실패 시 기본 요약 생성"""
        from services.record_service import RecordService
        return RecordService._generate_summary(content)
    
    @staticmethod
    def analyze_emotion_with_ai(content: str) -> Dict:
        """GPT-4o mini를 우선 사용하고, 실패 시 기본 분석 사용"""
        
        # GPT-4o mini 시도
        result = AIAnalysisService.analyze_emotion_with_gpt4o(content)
        if result:
            return AIAnalysisService._convert_ai_result_to_color(result)
        
        # 기본 분석 사용
        return AIAnalysisService.analyze_emotion_fallback(content)
    
    @staticmethod
    def generate_summary_with_ai(content: str) -> str:
        """GPT-4o mini를 우선 사용하고, 실패 시 기본 요약 사용"""
        
        # GPT-4o mini 시도
        summary = AIAnalysisService.generate_summary_with_gpt4o(content)
        if summary:
            return summary
        
        # 기본 요약 사용
        return AIAnalysisService.generate_summary_fallback(content)
    
    @staticmethod
    def extract_keywords_with_gpt(content: str) -> list:
        """GPT-4o mini를 사용한 감정 키워드 추출"""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                return []
            client = OpenAI(api_key=api_key)
            prompt = f"""
            다음 텍스트에서 감정과 관련된 핵심 키워드 3~5개만 뽑아줘. 쉼표로 구분해서 반환해줘.
            텍스트: {content}
            키워드:
            """
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=50
            )
            keywords_str = response.choices[0].message.content.strip()
            # 쉼표로 분리하여 리스트로 변환
            keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
            return keywords[:5]
        except Exception as e:
            print(f"GPT-4o mini 키워드 추출 오류: {str(e)}")
            return []
    
    @staticmethod
    def generate_average_color_name_with_gpt(emotion_records: list) -> str:
        """GPT-4o mini를 사용한 평균 색상 이름 생성"""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                return "평균 감정색"
            
            client = OpenAI(api_key=api_key)
            
            # 감정 기록 요약
            emotions_summary = []
            for record in emotion_records:
                emotion = record.get('emotion_analysis', {}).get('primary_emotion', '알 수 없음')
                color_name = record.get('emotion_analysis', {}).get('color', {}).get('name', '알 수 없음')
                emotions_summary.append(f"{emotion}({color_name})")
            
            emotions_text = ", ".join(emotions_summary)
            
            prompt = f"""
            다음 감정 기록들의 평균을 나타내는 색상 이름을 창의적으로 만들어주세요.
            
            감정 기록들: {emotions_text}
            기간: {len(emotion_records)}일간
            
            예시: "따뜻한 노랑", "차분한 파랑", "활기찬 주황" 등
            색상 이름만 반환해주세요. 다른 설명은 포함하지 마세요.
            """
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=30
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"GPT-4o mini 평균 색상 이름 생성 오류: {str(e)}")
            return "평균 감정색"
    
    @staticmethod
    def _convert_ai_result_to_color(ai_result: Dict) -> Dict:
        """AI 분석 결과를 색상 정보로 변환"""
        from services.emotion_color_service import EmotionColorService
        
        primary_emotion = ai_result.get("primary_emotion", "기쁨")
        intensity = ai_result.get("intensity", 5)
        ai_color_name = ai_result.get("color_name", "")
        
        # AI가 제공한 색상 이름이 있으면 사용, 없으면 기본 색상 사용
        if ai_color_name:
            color_info = EmotionColorService._get_color_with_intensity(primary_emotion, intensity)
            color_info["name"] = ai_color_name  # AI가 제공한 색상 이름으로 덮어쓰기
        else:
            color_info = EmotionColorService._get_color_with_intensity(primary_emotion, intensity)
        
        return {
            "primary_emotion": primary_emotion,
            "intensity": intensity,
            "confidence": ai_result.get("confidence", 0.5),
            "reasoning": ai_result.get("reasoning", ""),
            "color": color_info,
            "message": f"오늘의 감정색은 {color_info['name']}입니다~ (AI 분석)",
            "ai_used": True
        } 