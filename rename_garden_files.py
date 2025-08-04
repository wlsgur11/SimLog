import os
import re

def clean_filename(filename):
    """파일명을 깔끔하게 정리"""
    # 확장자 제거
    name, ext = os.path.splitext(filename)
    
    # 방향과 크기 정보 추출
    direction_match = re.search(r'Direction=([^,]+)', name)
    size_match = re.search(r'Size=([^,]+)', name)
    color_match = re.search(r'Color=([^,]+)', name)
    
    if direction_match and size_match:
        direction = direction_match.group(1).strip()
        size = size_match.group(1).strip()
        
        # 방향을 간단한 이름으로 변환
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
        
        # 크기를 간단한 이름으로 변환
        size_map = {
            'Regular': 'regular',
            'Small': 'small'
        }
        
        direction_clean = direction_map.get(direction, direction.lower().replace(' ', '_'))
        size_clean = size_map.get(size, size.lower())
        
        new_name = f"{direction_clean}_{size_clean}{ext}"
        return new_name
    
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

def main():
    base_dir = "frontend/assets/images/garden"
    
    # 색상별 폴더들
    color_dirs = [
        "colors/light_green",
        "colors/green", 
        "colors/dark_moss_green",
        "colors/moss_green"
    ]
    
    print("🌿 정원 에셋 파일명 변경을 시작합니다...")
    
    for color_dir in color_dirs:
        full_path = os.path.join(base_dir, color_dir)
        rename_files_in_directory(full_path)
    
    print("✅ 모든 파일명 변경이 완료되었습니다!")

if __name__ == "__main__":
    main() 