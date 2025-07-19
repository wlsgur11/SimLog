# SimLog Backend 설치 가이드

## 1. 의존성 설치

### 가상환경 활성화
```bash
cd backend
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 패키지 설치
```bash
pip install -r requirements.txt
```

또는 개별 설치:
```bash
pip install fastapi uvicorn sqlalchemy pymysql python-dotenv passlib python-jose python-multipart requests openai
```

## 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 추가:

```bash
# Database Configuration
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/simlog_db

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI API (GPT-4o mini)
OPENAI_API_KEY=sk-your-openai-api-key-here

# NAVER CLOVA Speech Recognition (선택사항)
CLOVA_CLIENT_ID=your-clova-client-id
CLOVA_CLIENT_SECRET=your-clova-client-secret
```

## 3. 데이터베이스 설정

### MySQL 테이블 생성
```sql
-- 외래키 제약 조건 비활성화
SET FOREIGN_KEY_CHECKS = 0;

-- 기존 테이블 삭제
DROP TABLE IF EXISTS records;
DROP TABLE IF EXISTS users;

-- 외래키 제약 조건 활성화
SET FOREIGN_KEY_CHECKS = 1;
```

### 또는 마이그레이션 스크립트 실행
```bash
python migrate_db.py
```

## 4. 서버 실행

```bash
uvicorn main:app --reload
```

## 5. API 테스트

### Swagger UI
```
http://localhost:8000/docs
```

### 주요 API 엔드포인트
- `POST /auth/signup` - 회원가입
- `POST /auth/login` - 로그인
- `POST /records/` - 감정 기록 생성
- `GET /emotions/analyze-ai` - AI 감정 분석
- `GET /emotions/summarize` - AI 텍스트 요약
- `POST /voice/speech-to-text` - 음성 인식

## 6. 문제 해결

### ModuleNotFoundError: No module named 'requests'
```bash
pip install requests
```

### ModuleNotFoundError: No module named 'openai'
```bash
pip install openai
```

### 데이터베이스 연결 오류
- MySQL 서버가 실행 중인지 확인
- DATABASE_URL 형식 확인
- 데이터베이스와 사용자 권한 확인 