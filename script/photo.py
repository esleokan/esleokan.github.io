#!/usr/bin/env python3
import os
import yaml
import json
from datetime import datetime

# 設定
FURSUIT_DATA_FILE = '_data/fursuit.yml'  # YAML 輸出檔案
FURSUIT_JSON_FILE = '_data/fursuit.json'  # JSON 輸出檔案 (備用)
FURSUIT_IMAGE_DIR = 'assets/images/fursuit'  # Fursuit 圖片目錄

# 確保目錄存在
os.makedirs(os.path.dirname(FURSUIT_DATA_FILE), exist_ok=True)
os.makedirs(FURSUIT_IMAGE_DIR, exist_ok=True)

def scan_images():
    """掃描圖片目錄並列出所有圖片檔案"""
    images = []
    
    if not os.path.exists(FURSUIT_IMAGE_DIR):
        print(f"錯誤: 找不到圖片目錄 {FURSUIT_IMAGE_DIR}")
        return images
    
    for filename in os.listdir(FURSUIT_IMAGE_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            image_path = os.path.join(FURSUIT_IMAGE_DIR, filename)
            images.append(image_path)
    
    return sorted(images)

def create_fursuit_data():
    """建立 Fursuit 資料"""
    images = scan_images()
    if not images:
        print(f"錯誤: 在 {FURSUIT_IMAGE_DIR} 目錄中找不到圖片")
        return []
    
    print(f"找到 {len(images)} 張圖片")
    
    fursuit_data = []
    
    for idx, image_path in enumerate(images, 1):
        filename = os.path.basename(image_path)
        print(f"\n處理圖片 {idx}/{len(images)}: {filename}")
        
        # 獲取攝影師
        photographer = input(f"請輸入圖片 {idx} 的攝影師名稱: ").strip()
        
        # 獲取拍攝時間
        while True:
            date_str = input(f"請輸入拍攝時間 (YYYY-MM-DD 或留空使用今天): ").strip()
            if not date_str:
                # 使用今天的日期
                date_taken = datetime.now().strftime('%Y-%m-%d')
                break
            
            # 嘗試解析輸入的日期
            try:
                # 簡單驗證格式
                if len(date_str.split('-')) != 3:
                    raise ValueError("格式不正確")
                
                year, month, day = map(int, date_str.split('-'))
                datetime(year, month, day)  # 驗證是否為有效日期
                date_taken = date_str
                break
            except Exception as e:
                print(f"無效的日期格式: {e}")
                print("請使用 YYYY-MM-DD 格式，例如 2025-03-25")
        
        # 獲取標題 (可選)
        title = input(f"請輸入圖片標題 (可選): ").strip()
        
        # 獲取描述 (可選)
        description = input(f"請輸入圖片描述 (可選): ").strip()
        
        # 建立項目數據
        item = {
            'image': f"/{image_path}",
            'photographer': photographer,
            'date_taken': date_taken
        }
        
        if title:
            item['title'] = title
        if description:
            item['description'] = description
        
        fursuit_data.append(item)
    
    return fursuit_data

def save_data(data, yaml_file, json_file=None):
    """儲存資料到 YAML 和可選的 JSON 檔案"""
    try:
        # 保存為 YAML
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        print(f"已儲存 YAML 檔案: {yaml_file}")
        
        # 如果提供了 JSON 檔案路徑，也保存為 JSON
        if json_file:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"已儲存 JSON 檔案: {json_file}")
                
        return True
    except Exception as e:
        print(f"儲存資料檔案時出錯: {e}")
        return False

def load_existing_data():
    """載入既有資料 (如果存在)"""
    if os.path.exists(FURSUIT_DATA_FILE):
        try:
            with open(FURSUIT_DATA_FILE, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            return data or []
        except Exception as e:
            print(f"讀取既有資料時出錯: {e}")
    return []

def main():
    print("=== Fursuit YAML 創建工具 ===")
    
    # 詢問圖片目錄位置
    global FURSUIT_IMAGE_DIR
    user_image_dir = input(f"圖片目錄 (預設: '{FURSUIT_IMAGE_DIR}'): ").strip()
    if user_image_dir:
        FURSUIT_IMAGE_DIR = user_image_dir
    
    # 詢問輸出檔案位置
    global FURSUIT_DATA_FILE, FURSUIT_JSON_FILE
    user_yaml_file = input(f"YAML 輸出檔案 (預設: '{FURSUIT_DATA_FILE}'): ").strip()
    if user_yaml_file:
        FURSUIT_DATA_FILE = user_yaml_file
    
    user_json_file = input(f"JSON 輸出檔案 (預設: '{FURSUIT_JSON_FILE}'): ").strip()
    if user_json_file:
        FURSUIT_JSON_FILE = user_json_file
    
    # 確認是否覆蓋現有資料
    existing_data = load_existing_data()
    if existing_data:
        print(f"找到既有資料：{len(existing_data)} 個項目")
        choice = input("要加入既有資料中還是創建新的檔案？ (A=加入, N=新建): ").strip().upper()
        
        if choice == 'A':
            print("將加入既有資料")
            new_data = create_fursuit_data()
            if new_data:
                combined_data = existing_data + new_data
                save_data(combined_data, FURSUIT_DATA_FILE, FURSUIT_JSON_FILE)
                print(f"已保存 {len(combined_data)} 個項目 ({len(existing_data)} 舊 + {len(new_data)} 新)")
            return
    
    # 創建新資料
    fursuit_data = create_fursuit_data()
    if fursuit_data:
        save_data(fursuit_data, FURSUIT_DATA_FILE, FURSUIT_JSON_FILE)
        print(f"已保存 {len(fursuit_data)} 個項目")

if __name__ == "__main__":
    main()
