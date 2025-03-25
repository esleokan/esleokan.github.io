#!/usr/bin/env python3
import csv
import os
import sys
import urllib.request
import urllib.parse
import concurrent.futures
from datetime import datetime
import yaml
import shutil
import hashlib

# 設定
CSV_FILE = '_data/gallery.csv'  # CSV 檔案路徑
IMAGE_DIR = 'assets/images/gallery'  # 圖片保存目錄
LOG_FILE = 'download_images.log'  # 日誌檔案
FILE_PREFIX = 'loyn_comm_'  # 檔案名稱前綴
MAX_WORKERS = 10  # 並發下載線程數
MAX_DOWNLOAD_SIZE = 20 * 1024 * 1024  # 20MB 最大檔案大小限制
RESIZE_WIDTH = 800  # 壓縮寬度限制

from PIL import Image
import io

def download_file(url, max_size=MAX_DOWNLOAD_SIZE):
    """
    安全下載檔案，確保完整性
    
    :param url: 下載 URL
    :param max_size: 最大檔案大小
    :return: 下載的檔案二進位數據
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'image/*'
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            # 檢查 Content-Length（如果存在）
            content_length = response.headers.get('Content-Length')
            if content_length and int(content_length) > max_size:
                raise ValueError(f"檔案過大: {content_length} 位元組")
            
            # 讀取資料
            data = response.read(max_size + 1)
            
            # 確保檔案大小在限制範圍內
            if len(data) > max_size:
                raise ValueError("下載檔案超過最大大小限制")
            
            # 驗證檔案完整性
            file_hash = hashlib.md5(data).hexdigest()
            
            return data, file_hash
    
    except Exception as e:
        print(f"下載失敗: {e}")
        return None, None

def resize_image(image_data, max_width=RESIZE_WIDTH):
    """
    等比例縮放圖片
    
    :param image_data: 圖片二進位數據
    :param max_width: 最大寬度
    :return: 調整大小後的圖片二進位數據
    """
    try:
        # 從記憶體開啟圖片
        with Image.open(io.BytesIO(image_data)) as img:
            # 計算等比例縮放
            width, height = img.size
            
            # 如果寬度已經小於等於目標寬度，直接返回原圖
            if width <= max_width:
                return image_data
            
            # 計算縮放比例
            ratio = max_width / width
            new_height = int(height * ratio)
            
            # 使用高品質插值
            resized_img = img.resize((max_width, new_height), Image.LANCZOS)
            
            # 儲存到記憶體
            output_buffer = io.BytesIO()
            
            # 根據原始圖片格式保存
            if img.format == 'PNG':
                resized_img.save(output_buffer, format='PNG', optimize=True)
            elif img.format == 'GIF':
                resized_img.save(output_buffer, format='GIF')
            else:
                resized_img.save(output_buffer, format='JPEG', quality=85, optimize=True)
            
            return output_buffer.getvalue()
    
    except Exception as e:
        print(f"圖片縮放失敗: {e}")
        return image_data

def download_image(idx, row):
    """
    下載單一圖片
    
    :param idx: 圖片索引
    :param row: CSV 行數據
    :return: 下載成功的 YAML 條目或 None
    """
    image_url = row.get('image_link', '').strip().strip('"')
    
    if not image_url:
        print(f"跳過 #{idx + 1}: 空的 image_link")
        return None
    
    # 檢查 URL 是否為 HTTP/HTTPS
    if not (image_url.startswith('http://') or image_url.startswith('https://')):
        print(f"跳過 #{idx + 1}: 不是有效的 HTTP/HTTPS URL: {image_url}")
        return None
    
    # 使用編號命名檔案 (從 CSV 第一筆資料開始，index 0)
    number = idx + 1
    
    # 從 URL 獲取副檔名
    url_path = urllib.parse.urlparse(image_url).path
    _, ext = os.path.splitext(url_path)
    
    # 如果沒有副檔名，使用 .jpg
    if not ext:
        ext = '.jpg'
    
    # 建立檔名: loyn_comm_1.jpg, loyn_comm_2.png 等
    filename = f"{FILE_PREFIX}{number}{ext}"
    temp_path = os.path.join('.', filename)  # 下載到當前目錄
    final_path = os.path.join(IMAGE_DIR, filename)  # 最終目標路徑
    
    print(f"下載 #{number}: {image_url} -> {temp_path}")
    print(f"  標題: {row.get('title', '無標題')}")
    
    try:
        # 確保目標目錄存在
        os.makedirs(IMAGE_DIR, exist_ok=True)
        
        # 下載檔案
        data, file_hash = download_file(image_url)
        
        if not data:
            print(f"  ✗ 下載失敗")
            return None
        
        # 先儲存原始檔案
        with open(temp_path, 'wb') as f:
            f.write(data)
        
        # 縮放圖片
        with open(temp_path, 'rb') as f:
            original_data = f.read()
        
        resized_data = resize_image(original_data)
        
        # 儲存縮放後的圖片到最終路徑
        with open(final_path, 'wb') as f:
            f.write(resized_data)
        
        # 刪除暫存檔案
        os.remove(temp_path)
        
        # 創建 YAML 條目
        yaml_entry = {
            'author': row.get('author', ''),
            'author_link': row.get('author_link', ''),
            'date_added': datetime.now().strftime('%Y-%m-%d'),
            'image': f'/assets/images/gallery/{filename}',
            'title': row.get('title', f'Artwork {number}')
        }
        
        print(f"  ✓ 成功下載並縮放: {final_path}")
        return yaml_entry
    
    except Exception as e:
        print(f"  ✗ 失敗 #{number}: {str(e)}")
        return None

def main():
    # 初始化日誌
    with open(LOG_FILE, 'w', encoding='utf-8') as log:
        log.write(f"開始下載和處理圖片: {datetime.now()}\n")
        log.write("----------------------------\n")

    try:
        # 讀取 CSV 數據（沿用之前的健壯讀取方法）
        with open(CSV_FILE, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
        
        if not rows:
            print("警告: CSV 檔案沒有數據")
            sys.exit(0)
        
        # 並發下載圖片
        yaml_entries = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_idx = {
                executor.submit(download_image, idx, row): idx 
                for idx, row in enumerate(rows)
            }
            
            for future in concurrent.futures.as_completed(future_to_idx):
                result = future.result()
                if result:
                    yaml_entries.append(result)
        
        # 排序 YAML 條目
        yaml_entries.sort(key=lambda x: int(x['image'].split('_')[-1].split('.')[0]))
        
        # 保存 YAML 文件
        yaml_path = '_data/gallery.yml'
        with open(yaml_path, 'w', encoding='utf-8') as yamlfile:
            yaml.safe_dump(yaml_entries, yamlfile, allow_unicode=True, default_flow_style=False)
        
        print(f"\n已生成 YAML 檔案: {yaml_path}")
        print(f"完成! 共處理 {len(rows)} 筆資料")

    except Exception as e:
        print(f"錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

    print(f"\n詳細日誌保存在: {LOG_FILE}")

if __name__ == "__main__":
    main()
