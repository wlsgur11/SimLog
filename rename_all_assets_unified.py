import os
import re

def clean_filename(filename, folder_path=""):
    """파일명을 통일된 컨벤션으로 정리"""
    # 확장자 제거
    name, ext = os.path.splitext(filename)
    
    # 폴더별 처리
    if "fishes" in folder_path:
        # 물고기: red.png, orange.png (이미 깔끔함)
        return filename
    
    elif "lotus" in folder_path:
        # 연꽃: moss_green.png, light_green.png (이미 깔끔함)
        return filename
    
    elif "flowers" in folder_path:
        if "single_flowers" in folder_path or "big_paddle" in folder_path:
            # 꽃: yellow_small_paddles.png (이미 깔끔함)
            return filename
        else:
            # 단순 꽃: yellow.png, purple.png (이미 깔끔함)
            return filename
    
    elif "rocks" in folder_path:
        # 돌/벽돌
        if "🪨 Rocks" in name:
            return "rocks.png"
        elif "🧱 Circle Bricks" in name:
            return "circle_bricks.png"
        elif "🧱 Bricks" in name:
            return "bricks.png"
    
    elif "bloom/option" in folder_path:
        # 꽃 피움 레벨
        bloom_match = re.search(r'Bloom Level=([^,]+)', name)
        color_match = re.search(r'Color=([^,]+)', name)
        
        if bloom_match and color_match:
            bloom_level = bloom_match.group(1).strip().lower()
            color = color_match.group(1).strip().lower()
            return f"{color}_{bloom_level}_bloom.png"
    
    elif "bloom/color" in folder_path:
        # 꽃 크기
        size_match = re.search(r'Size=([^,]+)', name)
        color_match = re.search(r'Color=([^,]+)', name)
        
        if size_match and color_match:
            size = size_match.group(1).strip().lower().replace(' ', '_')
            color = color_match.group(1).strip().lower()
            return f"{color}_{size}.png"
    
    elif "bridge" in folder_path:
        # 다리
        direction_match = re.search(r'Direction=([^,]+)', name)
        
        if direction_match:
            direction = direction_match.group(1).strip()
            direction_map = {
                '↕️ Vertical': 'vertical',
                '↔️ Horizontal': 'horizontal',
                '➡️ Right (Short)': 'right_short',
                '➡️ Right': 'right',
                '⬇️ Bottom (Short)': 'bottom_short',
                '⬇️ Bottom': 'bottom',
                '⬆️ Top (Short)': 'top_short',
                '⬆️ Top': 'top',
                '⬅️ Left (Short)': 'left_short',
                '⬅️ Left': 'left'
            }
            direction_clean = direction_map.get(direction, direction.lower().replace(' ', '_'))
            return f"bridge_{direction_clean}.png"
    
    elif "veggie/single" in folder_path:
        # 단일 채소
        type_match = re.search(r'Type=([^,]+)', name)
        
        if type_match:
            veggie_type = type_match.group(1).strip().lower().replace(' ', '_')
            return f"{veggie_type}.png"
    
    elif "veggie/veggie_option" in folder_path:
        # 채소 옵션
        type_match = re.search(r'Type=([^,]+)', name)
        
        if type_match:
            veggie_type = type_match.group(1).strip().lower().replace(' ', '_')
            return f"{veggie_type}_option.png"
    
    elif "pond/pond" in folder_path:
        # 연못
        direction_match = re.search(r'Direction=([^,]+)', name)
        
        if direction_match:
            direction = direction_match.group(1).strip()
            direction_map = {
                '🔄 Center': 'center',
                '↖️Top Left': 'top_left',
                '↙️ Bottom Left': 'bottom_left',
                '↘️ Bottom Right': 'bottom_right',
                '➡️ Right': 'right',
                '↗️ Top Right': 'top_right',
                '⬇️ Bottom': 'bottom',
                '⬆️ Top': 'top',
                '⬅️ Left': 'left'
            }
            direction_clean = direction_map.get(direction, direction.lower().replace(' ', '_'))
            return f"pond_{direction_clean}.png"
    
    elif "pond/water_color" in folder_path:
        # 물 색상
        color_match = re.search(r'Color Water=([^,]+)', name)
        
        if color_match:
            color = color_match.group(1).strip().lower().replace(' ', '_')
            return f"water_{color}.png"
    
    elif "pond/pond_borders" in folder_path:
        # 연못 테두리
        border_match = re.search(r'Border Option=([^,]+)', name)
        color_match = re.search(r'Color=([^,]+)', name)
        direction_match = re.search(r'Direction=([^,]+)', name)
        
        if border_match and color_match and direction_match:
            border_type = border_match.group(1).strip()
            color = color_match.group(1).strip().lower()
            direction = direction_match.group(1).strip()
            
            # 이모지 제거
            border_type = re.sub(r'[🌳🌿🌸🌺🌻🌼🌷🌹🌱🌲🌴🌵🌾🌿🍀🍁🍂🍃🍄🌰🌱🌲🌴🌵🌾🌿🍀🍁🍂🍃🍄🌰]', '', border_type).strip()
            
            direction_map = {
                '↖️Top Left': 'top_left',
                '↙️ Bottom Left': 'bottom_left',
                '↘️ Bottom Right': 'bottom_right',
                '➡️ Right': 'right',
                '↗️ Top Right': 'top_right',
                '⬇️ Bottom': 'bottom',
                '⬆️ Top': 'top',
                '⬅️ Left': 'left'
            }
            direction_clean = direction_map.get(direction, direction.lower().replace(' ', '_'))
            
            return f"pond_border_{color}_{direction_clean}.png"
    
    return filename

def rename_files_in_directory(directory):
    """디렉토리 내의 모든 파일 이름 변경"""
    if not os.path.exists(directory):
        print(f"디렉토리가 존재하지 않습니다: {directory}")
        return
    
    print(f"📁 {directory} 폴더의 파일명을 변경합니다...")
    
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            old_path = os.path.join(directory, filename)
            new_filename = clean_filename(filename, directory)
            new_path = os.path.join(directory, new_filename)
            
            if old_path != new_path and new_filename != filename:
                try:
                    os.rename(old_path, new_path)
                    print(f"  ✓ {filename} → {new_filename}")
                except Exception as e:
                    print(f"  ✗ {filename} 변경 실패: {e}")

def rename_all_assets():
    base_dir = "frontend/assets/images/garden"
    
    # 모든 하위 폴더들 (재귀적으로 처리)
    def process_directory(directory):
        if not os.path.exists(directory):
            return
        
        # 현재 디렉토리의 파일들 처리
        rename_files_in_directory(directory)
        
        # 하위 디렉토리들 처리
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                process_directory(item_path)
    
    print("🌿 모든 정원 에셋 파일명 변경을 시작합니다...")
    process_directory(base_dir)
    print("✅ 모든 파일명 변경이 완료되었습니다!")

if __name__ == "__main__":
    rename_all_assets() 