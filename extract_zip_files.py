import zipfile
import os

# 압축 파일들과 대상 폴더 매핑
zip_files = {
    "Garden This - The Game (Community) Light Green.zip": "colors/light_green",
    "Garden This - The Game (Community) Green.zip": "colors/green", 
    "Garden This - The Game (Community) Dark Moss Green.zip": "colors/dark_moss_green",
    "Garden This - The Game (Community) Moss Green.zip": "colors/moss_green"
}

def extract_zip_files():
    base_dir = "frontend/assets/images/garden"
    
    for zip_file, target_dir in zip_files.items():
        zip_path = os.path.join(base_dir, zip_file)
        extract_path = os.path.join(base_dir, target_dir)
        
        if os.path.exists(zip_path):
            try:
                # 대상 폴더 생성
                os.makedirs(extract_path, exist_ok=True)
                
                # 압축 파일 풀기
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                
                print(f"✓ {zip_file} → {target_dir}")
            except Exception as e:
                print(f"✗ {zip_file} 압축 해제 실패: {e}")
        else:
            print(f"⚠ 압축 파일을 찾을 수 없습니다: {zip_file}")
    
    print("모든 압축 파일 압축 해제가 완료되었습니다!")

if __name__ == "__main__":
    extract_zip_files() 