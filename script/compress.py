#!/usr/bin/env python3
import os
import subprocess
import glob
from concurrent.futures import ThreadPoolExecutor

# 設定
FURSUIT_IMAGE_DIR = 'assets/images/fursuit'  # Fursuit 圖片目錄
OUTPUT_DIR = FURSUIT_IMAGE_DIR  # 輸出到同一目錄
MAX_WIDTH = 1200  # 圖片最大寬度

# 確保目錄存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

def compress_image(image_path):
    """壓縮一張圖片到指定寬度"""
    filename = os.path.basename(image_path)
    output_path = os.path.join(OUTPUT_DIR, f"compressed_{filename}")
    temp_path = os.path.join(OUTPUT_DIR, f"temp_{filename}")
    
    try:
        # 取得圖片尺寸
        size_cmd = ['identify', '-format', '%w %h', image_path]
        result = subprocess.run(size_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"無法獲取圖片資訊: {image_path}")
            return False
        
        width, height = map(int, result.stdout.strip().split())
        
        # 如果圖片寬度已經小於等於最大寬度，不需要壓縮
        if width <= MAX_WIDTH:
            print(f"圖片已經符合要求 ({width}x{height}): {filename}")
            return True
        
        # 計算縮放比例和新高度
        ratio = MAX_WIDTH / width
        new_height = int(height * ratio)
        
        # 使用 ImageMagick 壓縮圖片
        compress_cmd = [
            'convert', image_path,
            '-resize', f'{MAX_WIDTH}x{new_height}>',  # 只縮小，不放大
            '-quality', '85',  # 品質設定
            temp_path
        ]
        
        subprocess.run(compress_cmd, check=True)
        
        # 獲取原始文件大小
        original_size = os.path.getsize(image_path) / 1024  # KB
        
        # 獲取壓縮後文件大小
        compressed_size = os.path.getsize(temp_path) / 1024  # KB
        
        # 替換原始文件
        os.rename(temp_path, image_path)
        
        # 輸出結果
        reduction = (1 - compressed_size / original_size) * 100
        print(f"壓縮成功: {filename}")
        print(f"  • 原始尺寸: {width}x{height}, {original_size:.1f} KB")
        print(f"  • 壓縮後: {MAX_WIDTH}x{new_height}, {compressed_size:.1f} KB")
        print(f"  • 減少: {reduction:.1f}%")
        
        return True
    except Exception as e:
        print(f"壓縮圖片失敗 {filename}: {e}")
        
        # 刪除臨時文件
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return False

def main():
    print("=== 圖片壓縮工具 (最大寬度 1200px) ===")
    
    # 詢問圖片目錄
    global FURSUIT_IMAGE_DIR, OUTPUT_DIR
    user_input = input(f"圖片目錄 (預設: '{FURSUIT_IMAGE_DIR}'): ").strip()
    if user_input:
        FURSUIT_IMAGE_DIR = user_input
        OUTPUT_DIR = user_input  # 更新輸出目錄
    
    # 獲取所有圖片
    supported_formats = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']
    image_files = []
    
    for format_pattern in supported_formats:
        pattern = os.path.join(FURSUIT_IMAGE_DIR, format_pattern)
        image_files.extend(glob.glob(pattern))
    
    if not image_files:
        print(f"找不到任何圖片在 {FURSUIT_IMAGE_DIR} 目錄中")
        return
    
    print(f"找到 {len(image_files)} 張圖片")
    
    # 詢問是否繼續
    choice = input(f"是否壓縮這些圖片？ (y/n): ").strip().lower()
    if choice != 'y':
        print("操作已取消")
        return
    
    # 使用多線程加速處理
    print(f"\n開始壓縮 {len(image_files)} 張圖片...")
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(executor.map(compress_image, image_files))
    
    # 統計結果
    success_count = results.count(True)
    fail_count = results.count(False)
    
    print(f"\n壓縮完成!")
    print(f"成功: {success_count} 張圖片")
    print(f"失敗: {fail_count} 張圖片")

if __name__ == "__main__":
    main()
