from typing import Dict, List, Tuple
import json

class EmotionColorService:
    """
    로버트 플루치크의 감정의 바퀴 기반 색상 매핑 서비스
    """
    
    # 8가지 기본 감정과 색상 매핑
    EMOTION_COLORS = {
        "기쁨": {
            "name": "파스텔 옐로우",
            "hex": "#FFE5B4",
            "rgb": (255, 229, 180),
            "description": "밝고 따뜻한 기쁨의 색"
        },
        "신뢰": {
            "name": "파스텔 그린",
            "hex": "#B8E6B8",
            "rgb": (184, 230, 184),
            "description": "안정감과 신뢰를 나타내는 색"
        },
        "두려움": {
            "name": "파스텔 그레이",
            "hex": "#D3D3D3",
            "rgb": (211, 211, 211),
            "description": "불안과 두려움을 나타내는 색"
        },
        "놀람": {
            "name": "파스텔 오렌지",
            "hex": "#FFD4B3",
            "rgb": (255, 212, 179),
            "description": "예상치 못한 놀람을 나타내는 색"
        },
        "슬픔": {
            "name": "파스텔 블루",
            "hex": "#B3D9FF",
            "rgb": (179, 217, 255),
            "description": "차분하고 슬픈 감정을 나타내는 색"
        },
        "혐오": {
            "name": "파스텔 브라운",
            "hex": "#D4C4A8",
            "rgb": (212, 196, 168),
            "description": "불쾌감과 혐오를 나타내는 색"
        },
        "분노": {
            "name": "파스텔 레드",
            "hex": "#FFB3B3",
            "rgb": (255, 179, 179),
            "description": "강렬한 분노를 나타내는 색"
        },
        "기대": {
            "name": "파스텔 퍼플",
            "hex": "#E6B3E6",
            "rgb": (230, 179, 230),
            "description": "희망과 기대를 나타내는 색"
        }
    }
    
    # 감정 강도별 색상 변화 (1-10점)
    INTENSITY_MODIFIERS = {
        1: {"name_suffix": " (매우 연함)", "brightness": 0.9},
        2: {"name_suffix": " (연함)", "brightness": 0.85},
        3: {"name_suffix": " (약간 연함)", "brightness": 0.8},
        4: {"name_suffix": " (보통)", "brightness": 0.75},
        5: {"name_suffix": " (보통)", "brightness": 0.7},
        6: {"name_suffix": " (보통)", "brightness": 0.65},
        7: {"name_suffix": " (약간 진함)", "brightness": 0.6},
        8: {"name_suffix": " (진함)", "brightness": 0.55},
        9: {"name_suffix": " (매우 진함)", "brightness": 0.5},
        10: {"name_suffix": " (최대)", "brightness": 0.45}
    }
    
    @staticmethod
    def get_emotion_colors() -> Dict:
        """모든 감정 색상 정보 반환"""
        return EmotionColorService.EMOTION_COLORS
    
    @staticmethod
    def analyze_emotion_from_text(content: str) -> Dict:
        """
        텍스트에서 감정을 분석하고 색상 정보를 반환
        (실제로는 외부 AI API를 사용할 예정)
        """
        # 임시 감정 분석 로직 (실제로는 AI API 사용)
        emotion_scores = EmotionColorService._analyze_emotion_keywords(content)
        
        # 가장 높은 점수의 감정 찾기
        primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        
        # 감정 강도 계산 (1-10)
        intensity = min(10, max(1, int(primary_emotion[1] * 10)))
        
        # 색상 정보 생성
        color_info = EmotionColorService._get_color_with_intensity(
            primary_emotion[0], intensity
        )
        
        return {
            "primary_emotion": primary_emotion[0],
            "emotion_scores": emotion_scores,
            "intensity": intensity,
            "color": color_info,
            "message": f"오늘의 감정색은 {color_info['name']}입니다~"
        }
    
    @staticmethod
    def _analyze_emotion_keywords(content: str) -> Dict[str, float]:
        """
        텍스트에서 감정 키워드를 분석하여 점수 반환
        (실제로는 AI API로 대체 예정)
        """
        emotion_keywords = {
            "기쁨": ["기쁘", "행복", "즐거", "웃", "신나", "좋", "만족", "감사"],
            "신뢰": ["믿", "안전", "안정", "확신", "신뢰", "의지"],
            "두려움": ["무서", "겁", "불안", "걱정", "두려", "떨", "긴장"],
            "놀람": ["놀라", "깜짝", "예상", "갑작", "충격", "놀람"],
            "슬픔": ["슬프", "우울", "속상", "서럽", "눈물", "비통", "허전"],
            "혐오": ["싫", "역겨", "불쾌", "짜증", "화나", "분노", "열받"],
            "분노": ["화나", "열받", "짜증", "분노", "화", "열", "폭발"],
            "기대": ["기대", "희망", "꿈", "미래", "계획", "준비", "새로운"]
        }
        
        scores = {emotion: 0.0 for emotion in emotion_keywords.keys()}
        
        # 각 감정별 키워드 검색
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    scores[emotion] += 0.3  # 키워드당 0.3점 추가
        
        # 최소 점수 보장
        if max(scores.values()) == 0:
            scores["기쁨"] = 0.1  # 기본값
        
        return scores
    
    @staticmethod
    def _get_color_with_intensity(emotion: str, intensity: int) -> Dict:
        """감정과 강도에 따른 색상 정보 반환"""
        if emotion not in EmotionColorService.EMOTION_COLORS:
            emotion = "기쁨"  # 기본값
        
        base_color = EmotionColorService.EMOTION_COLORS[emotion]
        modifier = EmotionColorService.INTENSITY_MODIFIERS.get(intensity, 
                                                              EmotionColorService.INTENSITY_MODIFIERS[5])
        
        # 강도에 따른 색상 조정
        adjusted_rgb = tuple(int(c * modifier["brightness"]) for c in base_color["rgb"])
        adjusted_hex = "#{:02x}{:02x}{:02x}".format(*adjusted_rgb)
        
        return {
            "name": base_color["name"] + modifier["name_suffix"],
            "hex": adjusted_hex,
            "rgb": adjusted_rgb,
            "description": base_color["description"],
            "intensity": intensity
        }
    
    @staticmethod
    def get_average_emotion_color(emotion_records: List[Dict]) -> Dict:
        """
        여러 감정 기록의 평균 색상 계산
        (일주일, 이주일, 한달간 통계용)
        """
        if not emotion_records:
            return EmotionColorService._get_color_with_intensity("기쁨", 5)
        
        # RGB 값들의 평균 계산
        total_r = sum(record["color"]["rgb"][0] for record in emotion_records)
        total_g = sum(record["color"]["rgb"][1] for record in emotion_records)
        total_b = sum(record["color"]["rgb"][2] for record in emotion_records)
        
        count = len(emotion_records)
        avg_rgb = (int(total_r / count), int(total_g / count), int(total_b / count))
        avg_hex = "#{:02x}{:02x}{:02x}".format(*avg_rgb)
        
        # 가장 가까운 감정 찾기
        closest_emotion = EmotionColorService._find_closest_emotion(avg_rgb)
        
        return {
            "name": f"평균 감정색 ({closest_emotion})",
            "hex": avg_hex,
            "rgb": avg_rgb,
            "description": f"지난 {count}일간의 평균 감정을 나타내는 색입니다.",
            "period": count,
            "closest_emotion": closest_emotion
        }
    
    @staticmethod
    def _find_closest_emotion(rgb: Tuple[int, int, int]) -> str:
        """RGB 값과 가장 가까운 감정 찾기"""
        min_distance = float('inf')
        closest_emotion = "기쁨"
        
        for emotion, color_info in EmotionColorService.EMOTION_COLORS.items():
            distance = sum((a - b) ** 2 for a, b in zip(rgb, color_info["rgb"]))
            if distance < min_distance:
                min_distance = distance
                closest_emotion = emotion
        
        return closest_emotion 