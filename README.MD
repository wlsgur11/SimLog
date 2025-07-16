# SimLog 프로젝트

## 개발 환경 및 주요 버전

- **FastAPI**: 0.115.8
- **Flutter**: 3.32.4 (channel stable)
- **Dart**: 3.8.1
- **DevTools**: 2.45.1
- **Android Studio**: 2024.3.2 Patch 1

---
## 프로젝트 소개
SimLog(심로그)는 감정 기록, AI 분석, 감정 정원 시각화, 위험 감정 감지 및 상담 연계 등 다양한 
심리 관리 기능을 제공하는 통합 정서관리 플랫폼입니다.


## 오늘의 개발 진행 내용 (2025-07-16)

### 1. 백엔드 회원가입/로그인 및 JWT 인증 구현
- FastAPI + MySQL + SQLAlchemy + JWT 기반 인증 시스템 구축
- 회원가입(/auth/signup), 로그인(/auth/login) API 구현
- 비밀번호 암호화(passlib), JWT 토큰 발급/검증

### 2. 마이페이지(회원정보) 기능 구현
- **내 정보 조회**: GET /users/me (JWT 인증 필요)
- **회원정보 수정**: PUT /users/me (닉네임, 비밀번호 등)
- **회원 탈퇴**: DELETE /users/me
- JWT 토큰 기반 인증 및 권한 처리

### 3. 테스트 방법
- Swagger UI(http://localhost:8000/docs)에서 API 테스트 가능
- Postman 등에서 access_token을 Authorization 헤더에 Bearer 방식으로 추가하여 테스트

### 4. 기타
- .env 환경변수 및 .gitignore 보안 설정
- 내부 모듈 import 구조(backend.패키지.모듈) 통일

---

## 폴더 구조
- backend/: FastAPI 기반 백엔드 서버
- frontend/: Flutter 기반 모바일/웹 프론트엔드
- docs/: 개발계획서, 참고자료 등 문서

## 시작 방법
(추후 각 환경별 실행 방법, 의존성 설치 방법 등 상세히 추가 예정)

다음은 