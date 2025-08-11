#!/usr/bin/env python3
"""
422 오류 해결을 위한 회원가입 테스트 스크립트
"""

import requests
import json

# Railway 백엔드 URL
BASE_URL = "https://simlog-production.up.railway.app"

def test_signup_with_validation():
    """데이터 검증을 고려한 회원가입 테스트"""
    
    # 다양한 테스트 데이터 (422 오류 해결)
    test_cases = [
        {
            "name": "완전한 데이터",
            "data": {
                "email": "test1@example.com",
                "password": "testpassword123",
                "nickname": "테스트사용자1"
            }
        },
        {
            "name": "최소 데이터",
            "data": {
                "email": "test2@example.com",
                "password": "123456",
                "nickname": "테스트2"
            }
        },
        {
            "name": "빈 데이터로 테스트",
            "data": {}
        }
    ]
    
    for test_case in test_cases:
        print(f"\n=== {test_case['name']} ===")
        
        try:
            # 회원가입 요청
            response = requests.post(
                f"{BASE_URL}/auth/signup",
                json=test_case['data'],
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Body: {response.text}")
            
            if response.status_code == 200:
                print("✅ 성공!")
            elif response.status_code == 422:
                print("⚠️ 데이터 검증 실패 (예상됨)")
                # 422 응답에서 상세한 오류 정보 확인
                try:
                    error_data = response.json()
                    print(f"오류 상세: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
                except:
                    print("JSON 파싱 실패")
            else:
                print("❌ 예상치 못한 오류")
                
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

def test_auth_schema():
    """인증 API 스키마 확인"""
    
    print("\n=== API 스키마 확인 ===")
    
    # OPTIONS 요청으로 API 스키마 확인
    try:
        response = requests.options(f"{BASE_URL}/auth/signup")
        print(f"Signup OPTIONS: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
    except Exception as e:
        print(f"OPTIONS 요청 실패: {e}")

if __name__ == "__main__":
    print("=== SimLog API 422 오류 해결 테스트 ===")
    print(f"Base URL: {BASE_URL}")
    
    test_auth_schema()
    test_signup_with_validation()
