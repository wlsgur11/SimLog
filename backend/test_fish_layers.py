#!/usr/bin/env python3
"""
물고기 아이템들의 레이어 할당을 테스트하는 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.garden_service import GardenService

def test_fish_layers():
    """물고기 아이템들의 레이어 할당을 테스트"""
    print("=== 물고기 레이어 테스트 ===")
    
    # 테스트할 물고기 아이템들
    fish_items = [
        "빨간 물고기",
        "주황 물고기",
        "파란 물고기",
        "노란 물고기",
        "초록 물고기",
        "보라 물고기",
        "검은 물고기",
        "흰 물고기"
    ]
    
    for fish_name in fish_items:
        layer = GardenService._get_item_layer(fish_name)
        print(f"{fish_name}: 레이어 {layer}")
        
        if layer == 3:
            print(f"  ✅ {fish_name}이 올바르게 레이어 3에 할당되었습니다.")
        else:
            print(f"  ❌ {fish_name}이 잘못된 레이어 {layer}에 할당되었습니다.")
    
    print("\n=== 다른 아이템들 테스트 ===")
    
    # 다른 아이템들도 테스트
    other_items = [
        "노란 꽃",
        "연못",
        "나무 다리",
        "잔디 배경",
        "새",
        "나비"
    ]
    
    for item_name in other_items:
        layer = GardenService._get_item_layer(item_name)
        print(f"{item_name}: 레이어 {layer}")

if __name__ == "__main__":
    test_fish_layers() 