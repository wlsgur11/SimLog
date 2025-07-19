# SimLog (심로그) 🌸

**심리 감정 기록 및 AI 분석 플랫폼**

감정 표현이 서툰 청년층을 위한 비대면·비실명 감정 기록 및 AI 기반 피드백 시스템

## 🚀 주요 기능

### 📝 감정 기록
- **텍스트/음성 입력**: 자유로운 감정 표현
- **AI 키워드 추출**: 자동 감정 키워드 생성
- **AI 요약**: 감정 기록 자동 요약
- **하루 제한**: 건강한 감정 기록 습관 형성

### 🎨 감정 분석
- **Robert Plutchik 감정의 바퀴**: 8가지 기본 감정 분석
- **파스텔 색상 매핑**: 감정별 아름다운 색상 표현
- **감정 강도 분석**: 1-10 단계 감정 강도 측정
- **AI 기반 분석**: GPT-4o mini를 활용한 정교한 감정 분석

### 🎤 음성 인식
- **NAVER CLOVA Speech Recognition**: 한국어 음성 인식
- **음성-텍스트 변환**: 말로 하는 감정 기록
- **음성-감정 분석**: 음성으로 감정 분석

### 📊 통계 및 시각화
- **기간별 조회**: 일/주/월/년 단위 감정 기록
- **감정 통계**: 감정 분포 및 트렌드 분석
- **개인화 인사이트**: 개인별 감정 패턴 분석

## 🛠 기술 스택

### Backend
- **FastAPI**: 0.115.13 - 고성능 Python 웹 프레임워크
- **MySQL**: 관계형 데이터베이스
- **SQLAlchemy**: ORM 및 데이터베이스 관리
- **JWT**: 토큰 기반 인증
- **OpenAI GPT-4o mini**: AI 감정 분석 및 요약
- **NAVER CLOVA**: 한국어 음성 인식

### Frontend (계획)
- **Flutter**: 3.32.4 - 크로스 플랫폼 모바일 앱
- **Dart**: 3.8.1 - 프로그래밍 언어

## 🏗 프로젝트 구조

```
SimLog/
├── backend/                 # FastAPI 백엔드
│   ├── controllers/         # API 엔드포인트
│   ├── models/             # 데이터베이스 모델
│   ├── services/           # 비즈니스 로직
│   ├── main.py            # 애플리케이션 진입점
│   └── requirements.txt   # Python 의존성
├── frontend/               # Flutter 프론트엔드 (계획)
└── docs/                  # 프로젝트 문서
```

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 저장소 클론
git clone [repository-url]
cd SimLog

# 백엔드 의존성 설치
cd backend
pip install -r requirements.txt
```

### 2. 환경 변수 설정
```bash
# backend/.env 파일 생성
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/simlog_db
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-your-openai-api-key
CLOVA_CLIENT_ID=your-clova-client-id
CLOVA_CLIENT_SECRET=your-clova-client-secret
```

### 3. 데이터베이스 설정
```bash
# MySQL 데이터베이스 생성
CREATE DATABASE simlog_db;

# 테이블 생성
python migrate_db.py
```

### 4. 개발자 계정 생성
```bash
python create_developer.py
```

### 5. 서버 실행
```bash
uvicorn main:app --reload
```

### 6. API 테스트
```
http://localhost:8000/docs  # Swagger UI
```

## 📋 API 엔드포인트

### 인증
- `POST /auth/signup` - 회원가입
- `POST /auth/login` - 로그인

### 감정 기록
- `POST /records/` - 감정 기록 생성
- `GET /records/` - 감정 기록 목록
- `PUT /records/{id}` - 감정 기록 수정
- `DELETE /records/{id}` - 감정 기록 삭제

### 감정 분석
- `GET /emotions/analyze` - 키워드 기반 감정 분석
- `GET /emotions/analyze-ai` - AI 기반 감정 분석
- `GET /emotions/summarize` - AI 텍스트 요약

### 음성 인식
- `POST /voice/speech-to-text` - 음성-텍스트 변환
- `POST /voice/voice-to-emotion` - 음성-감정 분석

## 👨‍💻 개발자 모드

개발 및 테스트를 위한 개발자 계정:
- **특권**: 하루 제한 없이 감정 기록 생성 가능

## 📊 개발 현황 (2025-07-19)

### ✅ 완료된 기능
- [x] 백엔드 환경 설정 및 기본 구조
- [x] 사용자 인증 시스템 (JWT)
- [x] 감정 기록 CRUD API
- [x] AI 기반 감정 분석 및 요약
- [x] 음성 인식 시스템
- [x] 감정 색상 매핑 시스템
- [x] 개발자 도구 및 디버깅

### 🔄 진행 중
- 사용자 프로필 관리 시스템

### 📋 계획된 기능
- 상담소 연동 시스템
- 소셜 로그인 (카카오, 네이버)
- Flutter 모바일 앱
- 고급 분석 및 인사이트

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 연락처

프로젝트 링크: [https://github.com/wlsgur11/SimLog](https://github.com/wlsgur11/SimLog)

---

**SimLog** - 당신의 감정을 아름답게 기록하세요 🌸 