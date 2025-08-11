#!/usr/bin/env python3
"""
상세한 회원가입 테스트 스크립트
"""

import requests
import json

# Railway 백엔드 URL
BASE_URL = "https://simlog-production.up.railway.app"

def test_signup_detailed():
    """상세한 회원가입 테스트"""
    
    # 다양한 테스트 데이터
    test_cases = [
        {
            "name": "기본 회원가입",
            "data": {
                "email": "test1@example.com",
                "password": "testpassword123",
                "nickname": "테스트사용자1"
            }
        },
        {
            "name": "간단한 데이터",
            "data": {
                "email": "test2@example.com",
                "password": "123456",
                "nickname": "테스트2"
            }
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
            else:
                print("❌ 실패")
                
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

def test_auth_endpoints():
    """인증 관련 엔드포인트 테스트"""
    
    endpoints = [
        "/auth/signup",
        "/auth/login",
        "/health"
    ]
    
    print("\n=== 엔드포인트 테스트 ===")
    
    for endpoint in endpoints:
        try:
            if endpoint == "/health":
                response = requests.get(f"{BASE_URL}{endpoint}")
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", json={})
            
            print(f"{endpoint}: {response.status_code}")
            
        except Exception as e:
            print(f"{endpoint}: 오류 - {e}")

if __name__ == "__main__":
    print("=== SimLog API 상세 테스트 ===")
    print(f"Base URL: {BASE_URL}")
    
    test_auth_endpoints()
    test_signup_detailed()
