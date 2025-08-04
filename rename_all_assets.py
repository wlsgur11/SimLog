import os
import re

def clean_filename(filename):
    """파일명을 깔끔하게 정리"""
    # 확장자 제거
    name, ext = os.path.splitext(filename)
    
    # 색상 정보 추출
    color_match = re.search(r'Color=([^,]+)', name)
    bloom_match = re.search(r'Bloom Type=([^,]+)', name)
    direction_match = re.search(r'Direction=([^,]+)', name)
    size_match = re.search(r'Size=([^,]+)', name)
    
    if color_match and bloom_match:
        # 꽃 파일들
        color = color_match.group(1).strip()
        bloom_type = bloom_match.group(1).strip()
        
        color_map = {
            'Yellow': 'yellow',
            'Purple': 'purple', 
            'Pink': 'pink',
            'White': 'white',
            'Peach': 'peach',
            'Blue': 'blue'
        }
        
        bloom_map = {
            'Small Paddles': 'small_paddles',
            'Big Paddles': 'big_paddles'
        }
        
        color_clean = color_map.get(color, color.lower().replace(' ', '_'))
        bloom_clean = bloom_map.get(bloom_type, bloom_type.lower().replace(' ', '_'))
        
        return f"{color_clean}_{bloom_clean}{ext}"
    
    elif color_match and direction_match and size_match:
        # 울타리 파일들
        color = color_match.group(1).strip()
        direction = direction_match.group(1).strip()
        size = size_match.group(1).strip()
        
        color_map = {
            'Light Green': 'light_green',
            'Green': 'green',
            'Dark Moss Green': 'dark_moss_green',
            'Moss Green': 'moss_green'
        }
        
        direction_map = {
            '↔️ Horizontal': 'horizontal',
            '↕️ Vertical': 'vertical',
            '↖️Top Left': 'top_left',
            '↗️ Top Right': 'top_right',
            '↘️ Bottom Right': 'bottom_right',
            '↙️ Bottom Left': 'bottom_left',
            '⏩️ Connector Right': 'connector_right',
            '⏪️ Connector Left': 'connector_left',
            '⏫️ Connector top': 'connector_top',
            '⏬️ Connector Bottom': 'connector_bottom',
            '➕ Connector All': 'connector_all',
            '➡️ Right (Short)': 'right_short',
            '➡️ Right': 'right',
            '⬅️ Left (Short)': 'left_short',
            '⬅️ Left': 'left',
            '⬆️ Top (Short)': 'top_short',
            '⬆️ Top': 'top',
            '⬇️ Bottom (Short)': 'bottom_short',
            '⬇️ Bottom': 'bottom'
        }
        
        size_map = {
            'Regular': 'regular',
            'Small': 'small'
        }
        
        color_clean = color_map.get(color, color.lower().replace(' ', '_'))
        direction_clean = direction_map.get(direction, direction.lower().replace(' ', '_'))
        size_clean = size_map.get(size, size.lower())
        
        return f"{direction_clean}_{size_clean}{ext}"
    
    elif color_match:
        # 단순 색상 파일들
        color = color_match.group(1).strip()
        color_map = {
            'Yellow': 'yellow',
            'Purple': 'purple',
            'Pink': 'pink',
            'White': 'white',
            'Peach': 'peach',
            'Blue': 'blue'
        }
        color_clean = color_map.get(color, color.lower().replace(' ', '_'))
        return f"{color_clean}{ext}"
    
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
            new_filename = clean_filename(filename)
            new_path = os.path.join(directory, new_filename)
            
            if old_path != new_path:
                try:
                    os.rename(old_path, new_path)
                    print(f"  ✓ {filename} → {new_filename}")
                except Exception as e:
                    print(f"  ✗ {filename} 변경 실패: {e}")

def rename_all_assets():
    base_dir = "frontend/assets/images/garden"
    
    # 모든 하위 폴더들
    subdirs = [
        "flowers",
        "flowers/single_flowers", 
        "flowers/big_paddle",
        "pots",
        "decorations",
        "rocks",
        "bloom",
        "bridge",
        "veggie",
        "fence",
        "pond",
        "bushes",
        "lotus",
        "fishes",
        "backgrounds",
        "ui"
    ]
    
    print("🌿 모든 정원 에셋 파일명 변경을 시작합니다...")
    
    for subdir in subdirs:
        full_path = os.path.join(base_dir, subdir)
        if os.path.exists(full_path):
            rename_files_in_directory(full_path)
        else:
            print(f"⚠ 폴더가 존재하지 않습니다: {subdir}")
    
    print("✅ 모든 파일명 변경이 완료되었습니다!")

if __name__ == "__main__":
    rename_all_assets() 