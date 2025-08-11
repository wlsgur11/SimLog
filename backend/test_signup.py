#!/usr/bin/env python3
"""
회원가입 테스트 스크립트
"""

import requests
import json

# Railway 백엔드 URL
BASE_URL = "https://simlog-production.up.railway.app"

def test_signup():
    """간단한 회원가입 테스트"""
    
    # 테스트 데이터
    test_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "nickname": "테스트사용자"
    }
    
    try:
        # 회원가입 요청
        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ 회원가입 성공!")
        else:
            print("❌ 회원가입 실패")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def test_health():
    """헬스체크 테스트"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Health Check 오류: {e}")

if __name__ == "__main__":
    print("=== SimLog API 테스트 ===")
    print(f"Base URL: {BASE_URL}")
    print()
    
    test_health()
    print()
    test_signup()
