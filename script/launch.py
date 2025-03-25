#!/usr/bin/env python3
import os
import sys
import yaml
import json
import shutil
import subprocess
import glob
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# 設定
GALLERY_DATA_FILE = '_data/gallery.yml'
GALLERY_JSON_FILE = '_data/gallery.json'
FURSUIT_DATA_FILE = '_data/fursuit.yml'
FURSUIT_JSON_FILE = '_data/fursuit.json'
GALLERY_IMAGE_DIR = 'assets/images/gallery'
FURSUIT_IMAGE_DIR = 'assets/images/fursuit'
MAX_WIDTH = 1200
QUALITY = 85

# 確保目錄和文件存在
for directory in [GALLERY_IMAGE_DIR, FURSUIT_IMAGE_DIR, os.path.dirname(GALLERY_DATA_FILE)]:
    os.makedirs(directory, exist_ok=True)

# 設定終端顏色
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}! {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def load_data(file_path):
    """載入 YAML 資料檔案，如果檔案不存在或格式錯誤，返回空列表"""
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump([], f, allow_unicode=True)
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or []
        return data
    except Exception as e:
        print_error(f"讀取資料檔案時出錯 ({file_path}): {e}")
        return []

def save_data(data, yaml_file, json_file=None):
    """儲存資料到 YAML 和可選的 JSON 檔案"""
    try:
        # 保存為 YAML
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        print_success(f"已儲存 YAML 檔案: {yaml_file}")
        
        # 如果提供了 JSON 檔案路徑，也保存為 JSON
        if json_file:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print_success(f"已儲存 JSON 檔案: {json_file}")
                
        return True
    except Exception as e:
        print_error(f"儲存資料檔案時出錯: {e}")
        return False

def compress_image(source_path, target_dir, filename):
    """壓縮圖片並返回輸出路徑"""
    # 確保目標目錄存在
    os.makedirs(target_dir, exist_ok=True)
    
    # 獲取副檔名
    _, ext = os.path.splitext(source_path)
    if not ext:
        ext = '.jpg'  # 預設副檔名
    
    # 建立完整的輸出路徑
    output_path = os.path.join(target_dir, f"{filename}{ext}")
    
    # 執行圖片壓縮 (使用 ImageMagick)
    try:
        # 取得圖片尺寸
        size_cmd = ['identify', '-format', '%w %h', source_path]
        result = subprocess.run(size_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print_warning(f"無法獲取圖片資訊，將使用預設壓縮設定")
            original_width = "未知"
            original_height = "未知"
            original_size = os.path.getsize(source_path) / 1024  # KB
        else:
            original_width, original_height = map(int, result.stdout.strip().split())
            original_size = os.path.getsize(source_path) / 1024  # KB
            
            # 如果圖片寬度已經小於等於最大寬度，不需要壓縮尺寸
            if original_width <= MAX_WIDTH:
                print_warning(f"圖片寬度已經小於等於 {MAX_WIDTH}px，僅優化品質")
        
        # 使用 ImageMagick 壓縮圖片
        compress_cmd = [
            'convert', source_path,
            '-resize', f'{MAX_WIDTH}x>',  # 只縮小，不放大
            '-quality', str(QUALITY),
            output_path
        ]
        
        subprocess.run(compress_cmd, check=True)
        
        # 獲取壓縮後信息
        compressed_size = os.path.getsize(output_path) / 1024  # KB
        
        # 如果有圖片尺寸信息，顯示壓縮信息
        if original_width != "未知":
            size_result = subprocess.run(['identify', '-format', '%w %h', output_path], 
                                        capture_output=True, text=True)
            if size_result.returncode == 0:
                new_width, new_height = map(int, size_result.stdout.strip().split())
                reduction = (1 - compressed_size / original_size) * 100
                
                print_success(f"圖片已壓縮: {os.path.basename(output_path)}")
                print(f"  • 原始尺寸: {original_width}x{original_height}, {original_size:.1f} KB")
                print(f"  • 壓縮後: {new_width}x{new_height}, {compressed_size:.1f} KB")
                print(f"  • 減少: {reduction:.1f}%")
            else:
                print_success(f"圖片已處理: {os.path.basename(output_path)}")
        else:
            print_success(f"圖片已處理: {os.path.basename(output_path)}")
        
        return output_path, True
    except Exception as e:
        print_error(f"圖片壓縮失敗: {e}")
        
        # 如果壓縮失敗，直接複製原始檔案
        try:
            shutil.copy2(source_path, output_path)
            print_warning(f"已複製原始圖片: {os.path.basename(output_path)}")
            return output_path, True
        except Exception as copy_e:
            print_error(f"複製圖片失敗: {copy_e}")
            return None, False

def get_next_number(data, prefix):
    """獲取下一個可用的編號"""
    used_numbers = set()
    
    for item in data:
        image_path = item.get('image', '')
        if prefix in image_path:
            # 嘗試從路徑中提取編號
            try:
                filename = os.path.basename(image_path)
                # 從檔名中移除副檔名
                base_name = os.path.splitext(filename)[0]
                # 提取編號部分
                number_part = base_name.replace(prefix, '')
                if number_part.isdigit():
                    used_numbers.add(int(number_part))
            except:
                pass
    
    # 如果沒有找到編號，從 1 開始
    if not used_numbers:
        return 1
    
    # 否則返回最大編號 + 1
    return max(used_numbers) + 1

def add_gallery_image():
    """添加新的 Gallery 圖片"""
    print_header("添加 Gallery 圖片")
    
    # 載入現有資料
    gallery_data = load_data(GALLERY_DATA_FILE)
    
    # 詢問添加方式
    print("\n添加方式:")
    print("1. 單一圖片")
    print("2. 批次添加多個圖片")
    
    choice = input("\n請選擇添加方式 (1-2): ").strip()
    
    if choice == '1':
        # 單一圖片模式
        image_path = input("\n請輸入原始圖片路徑: ").strip()
        if not os.path.exists(image_path):
            print_error(f"找不到檔案: {image_path}")
            return
        
        # 獲取下一個可用的編號
        next_number = get_next_number(gallery_data, 'loyn_comm_')
        
        # 壓縮圖片
        output_path, success = compress_image(
            image_path, 
            GALLERY_IMAGE_DIR, 
            f"loyn_comm_{next_number}"
        )
        
        if not success:
            print_error("處理圖片失敗，中止操作")
            return
        
        # 將輸出路徑轉換為網站使用的路徑格式
        filename = os.path.basename(output_path)
        web_path = f"/{GALLERY_IMAGE_DIR}/{filename}"
        
        # 獲取 metadata
        title = input("輸入作品標題: ").strip()
        work_link = input("輸入作品連結 (可選): ").strip()
        author = input("輸入繪師名稱: ").strip()
        author_link = input("輸入繪師連結 (可選): ").strip()
        
        # 創建新項目
        new_item = {
            'title': title,
            'image': web_path,
            'date_added': datetime.now().strftime('%Y-%m-%d'),
        }
        
        if author:
            new_item['author'] = author
        if work_link:
            new_item['work_link'] = work_link
        if author_link:
            new_item['author_link'] = author_link
        
        # 添加到資料中
        gallery_data.append(new_item)
        
        # 保存資料
        if save_data(gallery_data, GALLERY_DATA_FILE, GALLERY_JSON_FILE):
            print_success(f"已添加 Gallery 項目: {title}")
            print(f"總共有 {len(gallery_data)} 個 Gallery 項目")
        else:
            print_error("儲存資料失敗")
    
    elif choice == '2':
        # 批次模式
        source_dir = input("\n請輸入包含多個圖片的目錄: ").strip()
        if not os.path.exists(source_dir):
            print_error(f"找不到目錄: {source_dir}")
            return
        
        # 取得所有圖片檔案
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']:
            image_files.extend(glob.glob(os.path.join(source_dir, ext)))
            image_files.extend(glob.glob(os.path.join(source_dir, ext.upper())))
        
        if not image_files:
            print_error(f"在 {source_dir} 中找不到圖片檔案")
            return
        
        # 排序檔案
        image_files.sort()
        
        print_success(f"找到 {len(image_files)} 個圖片檔案")
        
        # 詢問是否要為所有圖片設置相同的作者和作者連結
        same_author = input("\n所有圖片的繪師是否相同？(y/n): ").strip().lower() == 'y'
        common_author = ""
        common_author_link = ""
        
        if same_author:
            common_author = input("請輸入繪師名稱: ").strip()
            common_author_link = input("請輸入繪師連結 (可選): ").strip()
        
        # 處理每個圖片
        for i, image_path in enumerate(image_files):
            print(f"\n處理圖片 {i+1}/{len(image_files)}: {os.path.basename(image_path)}")
            
            # 獲取下一個可用的編號
            next_number = get_next_number(gallery_data, 'loyn_comm_')
            
            # 壓縮圖片
            output_path, success = compress_image(
                image_path, 
                GALLERY_IMAGE_DIR, 
                f"loyn_comm_{next_number}"
            )
            
            if not success:
                print_warning(f"處理圖片 {os.path.basename(image_path)} 失敗，跳過此圖片")
                continue
            
            # 將輸出路徑轉換為網站使用的路徑格式
            filename = os.path.basename(output_path)
            web_path = f"/{GALLERY_IMAGE_DIR}/{filename}"
            
            # 獲取 metadata
            if same_author:
                author = common_author
                author_link = common_author_link
            else:
                author = input("輸入繪師名稱: ").strip()
                author_link = input("輸入繪師連結 (可選): ").strip()
            
            title = input("輸入作品標題: ").strip()
            work_link = input("輸入作品連結 (可選): ").strip()
            
            # 創建新項目
            new_item = {
                'title': title,
                'image': web_path,
                'date_added': datetime.now().strftime('%Y-%m-%d'),
            }
            
            if author:
                new_item['author'] = author
            if work_link:
                new_item['work_link'] = work_link
            if author_link:
                new_item['author_link'] = author_link
            
            # 添加到資料中
            gallery_data.append(new_item)
        
        # 保存資料
        if save_data(gallery_data, GALLERY_DATA_FILE, GALLERY_JSON_FILE):
            print_success(f"\n已添加 {len(image_files)} 個 Gallery 項目")
            print(f"總共有 {len(gallery_data)} 個 Gallery 項目")
        else:
            print_error("儲存資料失敗")
    
    else:
        print_error("無效的選擇")

def add_fursuit_image():
    """添加新的 Fursuit 圖片"""
    print_header("添加 Fursuit 圖片")
    
    # 載入現有資料
    fursuit_data = load_data(FURSUIT_DATA_FILE)
    
    # 詢問添加方式
    print("\n添加方式:")
    print("1. 單一圖片")
    print("2. 批次添加多個圖片")
    
    choice = input("\n請選擇添加方式 (1-2): ").strip()
    
    if choice == '1':
        # 單一圖片模式
        image_path = input("\n請輸入原始圖片路徑: ").strip()
        if not os.path.exists(image_path):
            print_error(f"找不到檔案: {image_path}")
            return
        
        # 獲取下一個可用的編號
        next_number = get_next_number(fursuit_data, 'loyn_fursuit_')
        
        # 壓縮圖片
        output_path, success = compress_image(
            image_path, 
            FURSUIT_IMAGE_DIR, 
            f"loyn_fursuit_{next_number}"
        )
        
        if not success:
            print_error("處理圖片失敗，中止操作")
            return
        
        # 將輸出路徑轉換為網站使用的路徑格式
        filename = os.path.basename(output_path)
        web_path = f"/{FURSUIT_IMAGE_DIR}/{filename}"
        
        # 獲取 metadata
        photographer = input("輸入攝影師名稱: ").strip()
        
        date_str = input("輸入拍攝日期 YYYY-MM-DD (留空使用今天): ").strip()
        if not date_str:
            date_taken = datetime.now().strftime('%Y-%m-%d')
        else:
            date_taken = date_str
        
        title = input("輸入圖片標題 (可選): ").strip()
        description = input("輸入圖片描述 (可選): ").strip()
        
        # 創建新項目
        new_item = {
            'image': web_path,
            'photographer': photographer,
            'date_taken': date_taken,
            'date_added': datetime.now().strftime('%Y-%m-%d'),
        }
        
        if title:
            new_item['title'] = title
        if description:
            new_item['description'] = description
        
        # 添加到資料中
        fursuit_data.append(new_item)
        
        # 保存資料
        if save_data(fursuit_data, FURSUIT_DATA_FILE, FURSUIT_JSON_FILE):
            print_success(f"已添加 Fursuit 項目")
            print(f"總共有 {len(fursuit_data)} 個 Fursuit 項目")
        else:
            print_error("儲存資料失敗")
    
    elif choice == '2':
        # 批次模式
        source_dir = input("\n請輸入包含多個圖片的目錄: ").strip()
        if not os.path.exists(source_dir):
            print_error(f"找不到目錄: {source_dir}")
            return
        
        # 取得所有圖片檔案
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']:
            image_files.extend(glob.glob(os.path.join(source_dir, ext)))
            image_files.extend(glob.glob(os.path.join(source_dir, ext.upper())))
        
        if not image_files:
            print_error(f"在 {source_dir} 中找不到圖片檔案")
            return
        
        # 排序檔案
        image_files.sort()
        
        print_success(f"找到 {len(image_files)} 個圖片檔案")
        
        # 詢問是否要為所有圖片設置相同的攝影師和拍攝日期
        same_photographer = input("\n所有圖片的攝影師是否相同？(y/n): ").strip().lower() == 'y'
        common_photographer = ""
        common_date = ""
        
        if same_photographer:
            common_photographer = input("請輸入攝影師名稱: ").strip()
            date_str = input("輸入拍攝日期 YYYY-MM-DD (留空使用今天): ").strip()
            common_date = date_str or datetime.now().strftime('%Y-%m-%d')
        
        # 是否有共同標題或描述
        common_title_choice = input("\n這些圖片有共同的標題或描述嗎？(y/n): ").strip().lower() == 'y'
        common_title = ""
        common_description = ""
        
        if common_title_choice:
            common_title = input("請輸入共同的標題 (可選): ").strip()
            common_description = input("請輸入共同的描述 (可選): ").strip()
        
        # 處理每個圖片
        for i, image_path in enumerate(image_files):
            print(f"\n處理圖片 {i+1}/{len(image_files)}: {os.path.basename(image_path)}")
            
            # 獲取下一個可用的編號
            next_number = get_next_number(fursuit_data, 'loyn_fursuit_')
            
            # 壓縮圖片
            output_path, success = compress_image(
                image_path, 
                FURSUIT_IMAGE_DIR, 
                f"loyn_fursuit_{next_number}"
            )
            
            if not success:
                print_warning(f"處理圖片 {os.path.basename(image_path)} 失敗，跳過此圖片")
                continue
            
            # 將輸出路徑轉換為網站使用的路徑格式
            filename = os.path.basename(output_path)
            web_path = f"/{FURSUIT_IMAGE_DIR}/{filename}"
            
            # 獲取 metadata
            if same_photographer:
                photographer = common_photographer
                date_taken = common_date
            else:
                photographer = input("輸入攝影師名稱: ").strip()
                date_str = input("輸入拍攝日期 YYYY-MM-DD (留空使用今天): ").strip()
                date_taken = date_str or datetime.now().strftime('%Y-%m-%d')
            
            if common_title_choice:
                title = common_title
                description = common_description
            else:
                title = input("輸入圖片標題 (可選): ").strip()
                description = input("輸入圖片描述 (可選): ").strip()
            
            # 創建新項目
            new_item = {
                'image': web_path,
                'photographer': photographer,
                'date_taken': date_taken,
                'date_added': datetime.now().strftime('%Y-%m-%d'),
            }
            
            if title:
                new_item['title'] = title
            if description:
                new_item['description'] = description
            
            # 添加到資料中
            fursuit_data.append(new_item)
        
        # 保存資料
        if save_data(fursuit_data, FURSUIT_DATA_FILE, FURSUIT_JSON_FILE):
            print_success(f"\n已添加 {len(image_files)} 個 Fursuit 項目")
            print(f"總共有 {len(fursuit_data)} 個 Fursuit 項目")
        else:
            print_error("儲存資料失敗")
    
    else:
        print_error("無效的選擇")

def optimize_existing_images():
    """優化現有的圖片"""
    print_header("優化現有圖片")
    
    print("\n選擇要優化的圖片類型:")
    print("1. Gallery 圖片")
    print("2. Fursuit 圖片")
    print("3. 兩者都優化")
    
    choice = input("\n請選擇 (1-3): ").strip()
    
    if choice in ['1', '3']:
        optimize_directory(GALLERY_IMAGE_DIR, "Gallery")
    
    if choice in ['2', '3']:
        optimize_directory(FURSUIT_IMAGE_DIR, "Fursuit")
    
    print_success("圖片優化完成")

def optimize_directory(directory, type_name):
    """優化指定目錄中的所有圖片"""
    print(f"\n開始優化 {type_name} 圖片...")
    
    # 確保目錄存在
    if not os.path.exists(directory):
        print_error(f"目錄不存在: {directory}")
        return
    
    # 獲取所有圖片
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']:
        image_files.extend(glob.glob(os.path.join(directory, ext)))
        image_files.extend(glob.glob(os.path.join(directory, ext.upper())))
    
    if not image_files:
        print_warning(f"在 {directory} 中找不到圖片")
        return
    
    print(f"找到 {len(image_files)} 張 {type_name} 圖片")
    choice = input(f"是否要優化這些圖片？(y/n): ").strip().lower()
    
    if choice != 'y':
        print("已取消優化")
        return
    
    # 創建臨時目錄
    temp_dir = os.path.join(directory, "temp_optimized")
    os.makedirs(temp_dir, exist_ok=True)
    
    # 處理每個圖片
    for i, image_path in enumerate(image_files):
        filename = os.path.basename(image_path)
        print(f"\n處理圖片 {i+1}/{len(image_files)}: {filename}")
        
        # 獲取圖片尺寸
        try:
            size_cmd = ['identify', '-format', '%w %h', image_path]
            result = subprocess.run(size_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print_warning(f"無法獲取圖片資訊，將使用預設壓縮設定")
                original_width = "未知"
                original_height = "未知"
            else:
                original_width, original_height = map(int, result.stdout.strip().split())
                
                # 如果圖片寬度已經小於等於最大寬度，不需要壓縮尺寸
                if original_width <= MAX_WIDTH:
                    print_warning(f"圖片寬度已經小於等於 {MAX_WIDTH}px，僅優化品質")
            
            # 原始檔案大小
            original_size = os.path.getsize(image_path) / 1024  # KB
            
            # 臨時輸出路徑
            temp_path = os.path.join(temp_dir, filename)
            
            # 執行壓縮
            subprocess.run([
                'convert', image_path,
                '-resize', f'{MAX_WIDTH}x>',
                '-quality', str(QUALITY),
                temp_path
            ], check=True)
            
            # 新檔案大小
            new_size = os.path.getsize(temp_path) / 1024  # KB
            
            # 如果優化後的檔案比原始檔案小，才替換
            if new_size < original_size:
                reduction = (1 - new_size / original_size) * 100
                
                # 獲取新尺寸
                if original_width != "未知":
                    size_result = subprocess.run(['identify', '-format', '%w %h', temp_path], 
                                                capture_output=True, text=True)
                    if size_result.returncode == 0:
                        new_width, new_height = map(int, size_result.stdout.strip().split())
                        print_success(f"圖片已優化: {filename}")
                        print(f"  • 原始尺寸: {original_width}x{original_height}, {original_size:.1f} KB")
                        print(f"  • 優化後: {new_width}x{new_height}, {new_size:.1f} KB")
                        print(f"  • 減少: {reduction:.1f}%")
                
                # 替換原始檔案
                shutil.move(temp_path, image_path)
            else:
                print_warning(f"優化無效果，保留原始檔案: {filename}")
                os.remove(temp_path)
            
        except Exception as e:
            print_error(f"處理圖片失敗: {filename}, 錯誤: {e}")
    
    # 清理臨時目錄
    try:
        os.rmdir(temp_dir)
    except:
        pass

def modify_data_files():
    """修改資料檔案"""
    print_header("修改資料檔案")
    
    print("\n選擇要修改的資料檔案:")
    print("1. Gallery 資料")
    print("2. Fursuit 資料")
    
    choice = input("\n請選擇 (1-2): ").strip()
    
    if choice == '1':
        modify_data(GALLERY_DATA_FILE, GALLERY_JSON_FILE, 'Gallery')
    elif choice == '2':
        modify_data(FURSUIT_DATA_FILE, FURSUIT_JSON_FILE, 'Fursuit')
    else:
        print_error("無效的選擇")


def modify_data(yaml_file, json_file, type_name):
    """修改特定的資料檔案"""
    print(f"\n修改 {type_name} 資料...")
    
    # 載入資料
    data = load_data(yaml_file)
    
    if not data:
        print_warning(f"{type_name} 資料為空")
        return
    
    print(f"載入了 {len(data)} 個 {type_name} 項目")
    
    print("\n請選擇操作:")
    print("1. 修改單一項目")
    print("2. 刪除項目")
    print("3. 重新排序項目")
    print("4. 查看所有項目")
    
    choice = input("\n請選擇 (1-4): ").strip()
    
    if choice == '1':
        # 修改單一項目
        show_all_items(data, type_name)
        item_index = int(input("\n請輸入要修改的項目編號 (1-{}): ".format(len(data)))) - 1
        
        if item_index < 0 or item_index >= len(data):
            print_error("無效的項目編號")
            return
        
        # 顯示當前項目
        print("\n當前項目:")
        for key, value in data[item_index].items():
            print(f"  • {key}: {value}")
        
        # 詢問要修改的欄位
        print("\n請輸入要修改的欄位名稱 (例如 title, author 等):")
        field = input("欄位名: ").strip()
        
        if field in data[item_index] or field == 'new':
            if field == 'new':
                # 添加新欄位
                new_field = input("新欄位名稱: ").strip()
                new_value = input(f"{new_field} 的值: ").strip()
                data[item_index][new_field] = new_value
                print_success(f"已添加欄位 {new_field}")
            else:
                # 修改現有欄位
                current_value = data[item_index].get(field, "")
                new_value = input(f"當前值 '{current_value}', 新值: ").strip()
                
                if new_value:
                    data[item_index][field] = new_value
                    print_success(f"已更新 {field}")
                else:
                    # 如果輸入為空，詢問是否刪除欄位
                    delete = input("輸入為空，是否刪除此欄位？(y/n): ").strip().lower() == 'y'
                    if delete:
                        del data[item_index][field]
                        print_success(f"已刪除欄位 {field}")
        else:
            print_error(f"項目中沒有 {field} 欄位")
    
    elif choice == '2':
        # 刪除項目
        show_all_items(data, type_name)
        item_index = int(input("\n請輸入要刪除的項目編號 (1-{}): ".format(len(data)))) - 1
        
        if item_index < 0 or item_index >= len(data):
            print_error("無效的項目編號")
            return
        
        # 顯示要刪除的項目
        print("\n要刪除的項目:")
        for key, value in data[item_index].items():
            print(f"  • {key}: {value}")
        
        # 確認刪除
        confirm = input("確定要刪除此項目？(y/n): ").strip().lower() == 'y'
        
        if confirm:
            data.pop(item_index)
            print_success("項目已刪除")
        else:
            print("已取消刪除")
    
    elif choice == '3':
        # 重新排序
        print("\n排序方式:")
        print("1. 按添加日期 (新到舊)")
        print("2. 按添加日期 (舊到新)")
        print("3. 按標題字母順序")
        
        sort_choice = input("\n請選擇排序方式 (1-3): ").strip()
        
        if sort_choice == '1':
            # 按添加日期 (新到舊)
            data.sort(key=lambda x: x.get('date_added', ''), reverse=True)
            print_success("已按添加日期排序 (新到舊)")
        elif sort_choice == '2':
            # 按添加日期 (舊到新)
            data.sort(key=lambda x: x.get('date_added', ''))
            print_success("已按添加日期排序 (舊到新)")
        elif sort_choice == '3':
            # 按標題字母順序
            data.sort(key=lambda x: x.get('title', '').lower())
            print_success("已按標題字母順序排序")
        else:
            print_error("無效的選擇")
            return
    
    elif choice == '4':
        # 查看所有項目
        show_all_items(data, type_name)
        input("\n按 Enter 返回主選單...")
        return
    
    else:
        print_error("無效的選擇")
        return
    
    # 保存修改
    save_data(data, yaml_file, json_file)

def show_all_items(data, type_name):
    """顯示所有項目的基本資訊"""
    print(f"\n所有 {type_name} 項目:")
    
    for i, item in enumerate(data):
        title = item.get('title', '[無標題]')
        image = item.get('image', '[無圖片]')
        
        if type_name == 'Gallery':
            author = item.get('author', '[無作者]')
            print(f"{i+1}. {title} (by {author})")
        else:  # Fursuit
            photographer = item.get('photographer', '[無攝影師]')
            date = item.get('date_taken', '[無日期]')
            print(f"{i+1}. {title} (by {photographer}, {date})")
        
        print(f"   圖片: {image}")
        print()

def build_site():
    """建立網站"""
    print_header("建立網站")
    
    try:
        print("執行 Jekyll 建立...")
        result = subprocess.run(['bundle', 'exec', 'jekyll', 'build'], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        print_success("網站建立成功!")
    except subprocess.CalledProcessError as e:
        print_error(f"網站建立失敗: {e}")
        print(e.stdout)
        print(e.stderr)
    except Exception as e:
        print_error(f"執行命令時出錯: {e}")

def serve_site():
    """啟動本地伺服器"""
    print_header("啟動本地伺服器")
    
    try:
        print("啟動 Jekyll 伺服器...")
        print("請在瀏覽器中訪問 http://localhost:4000")
        print("按 Ctrl+C 停止伺服器")
        
        # 由於這會阻塞，不捕獲輸出
        subprocess.run(['bundle', 'exec', 'jekyll', 'serve'], check=True)
    except KeyboardInterrupt:
        print("\n已停止伺服器")
    except subprocess.CalledProcessError as e:
        print_error(f"啟動伺服器失敗: {e}")
    except Exception as e:
        print_error(f"執行命令時出錯: {e}")

def repair_data_files():
    """修復資料檔案"""
    print_header("修復資料檔案")
    
    print("\n選擇要修復的資料檔案:")
    print("1. Gallery 資料")
    print("2. Fursuit 資料")
    print("3. 兩者都修復")
    
    choice = input("\n請選擇 (1-3): ").strip()
    
    if choice in ['1', '3']:
        repair_file(GALLERY_DATA_FILE, GALLERY_JSON_FILE, 'Gallery')
    
    if choice in ['2', '3']:
        repair_file(FURSUIT_DATA_FILE, FURSUIT_JSON_FILE, 'Fursuit')
    
    print_success("修復完成")

def repair_file(yaml_file, json_file, type_name):
    """修復特定的資料檔案"""
    print(f"\n修復 {type_name} 資料檔案...")
    
    try:
        # 嘗試讀取 YAML
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not isinstance(data, list):
                print_error(f"YAML 檔案格式不正確，將創建新檔案")
                data = []
        except Exception as e:
            print_error(f"讀取 YAML 檔案失敗: {e}")
            data = []
        
        # 如果 YAML 為空，嘗試從 JSON 讀取
        if not data and os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if isinstance(data, list):
                    print_success(f"從 JSON 檔案恢復了 {len(data)} 個項目")
            except Exception as e:
                print_error(f"讀取 JSON 檔案失敗: {e}")
        
        # 修復每個項目
        fixed_items = []
        for item in data:
            if not isinstance(item, dict):
                print_warning(f"跳過無效項目: {item}")
                continue
            
            fixed_items.append(item)
        
        # 保存修復後的檔案
        save_data(fixed_items, yaml_file, json_file)
        print_success(f"已修復 {type_name} 資料檔案，保留了 {len(fixed_items)} 個項目")
    
    except Exception as e:
        print_error(f"修復 {type_name} 資料檔案失敗: {e}")

def export_data():
    """匯出資料為其他格式"""
    print_header("匯出資料")
    
    print("\n選擇要匯出的資料:")
    print("1. Gallery 資料")
    print("2. Fursuit 資料")
    
    data_choice = input("\n請選擇 (1-2): ").strip()
    
    if data_choice == '1':
        data_file = GALLERY_DATA_FILE
        type_name = 'Gallery'
    elif data_choice == '2':
        data_file = FURSUIT_DATA_FILE
        type_name = 'Fursuit'
    else:
        print_error("無效的選擇")
        return
    
    # 載入資料
    data = load_data(data_file)
    
    if not data:
        print_warning(f"{type_name} 資料為空")
        return
    
    print(f"載入了 {len(data)} 個 {type_name} 項目")
    
    print("\n選擇匯出格式:")
    print("1. CSV 格式")
    print("2. JSON 格式 (美化)")
    print("3. Markdown 列表")
    
    format_choice = input("\n請選擇 (1-3): ").strip()
    
    # 詢問輸出檔案
    output_file = input("\n請輸入輸出檔案名稱: ").strip()
    
    if not output_file:
        print_error("檔案名稱不能為空")
        return
    
    if format_choice == '1':
        # CSV 格式
        export_to_csv(data, output_file, type_name)
    elif format_choice == '2':
        # JSON 格式 (美化)
        export_to_json(data, output_file)
    elif format_choice == '3':
        # Markdown 列表
        export_to_markdown(data, output_file, type_name)
    else:
        print_error("無效的選擇")

def export_to_csv(data, output_file, type_name):
    """匯出資料為 CSV 格式"""
    import csv
    
    if not output_file.endswith('.csv'):
        output_file += '.csv'
    
    try:
        # 取得所有可能的欄位
        fields = set()
        for item in data:
            fields.update(item.keys())
        
        # 排序欄位，確保關鍵欄位在前
        priority_fields = ['title', 'image', 'author', 'photographer', 'date_taken', 'date_added']
        sorted_fields = []
        
        # 優先處理關鍵欄位
        for field in priority_fields:
            if field in fields:
                sorted_fields.append(field)
                fields.remove(field)
        
        # 添加剩餘欄位
        sorted_fields.extend(sorted(fields))
        
        # 寫入 CSV
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=sorted_fields)
            writer.writeheader()
            writer.writerows(data)
        
        print_success(f"已匯出 {len(data)} 個項目至 {output_file}")
    
    except Exception as e:
        print_error(f"匯出 CSV 失敗: {e}")

def export_to_json(data, output_file):
    """匯出資料為 JSON 格式 (美化)"""
    if not output_file.endswith('.json'):
        output_file += '.json'
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print_success(f"已匯出 {len(data)} 個項目至 {output_file}")
    
    except Exception as e:
        print_error(f"匯出 JSON 失敗: {e}")

def export_to_markdown(data, output_file, type_name):
    """匯出資料為 Markdown 列表"""
    if not output_file.endswith('.md'):
        output_file += '.md'
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {type_name} 列表\n\n")
            f.write(f"共 {len(data)} 個項目，生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for i, item in enumerate(data):
                f.write(f"## {i+1}. ")
                
                if 'title' in item and item['title']:
                    f.write(f"{item['title']}\n\n")
                else:
                    f.write(f"[無標題項目]\n\n")
                
                # 添加圖片
                if 'image' in item:
                    f.write(f"![圖片]({item['image']})\n\n")
                
                # 添加其他資訊
                for key, value in item.items():
                    if key not in ['title', 'image']:
                        f.write(f"- **{key}**: {value}\n")
                
                f.write("\n---\n\n")
        
        print_success(f"已匯出 {len(data)} 個項目至 {output_file}")
    
    except Exception as e:
        print_error(f"匯出 Markdown 失敗: {e}")

def check_dependencies():
    """檢查依賴是否已安裝"""
    print_header("檢查依賴")
    
    # 檢查 ImageMagick
    try:
        result = subprocess.run(['convert', '-version'], 
                              capture_output=True, text=True)
        
        if 'ImageMagick' in result.stdout:
            print_success("ImageMagick 已安裝")
        else:
            print_warning("無法確認 ImageMagick 安裝狀態")
    except:
        print_error("ImageMagick 未安裝或無法執行")
        print("請安裝 ImageMagick:")
        print("  • Ubuntu/Debian: sudo apt install imagemagick")
        print("  • macOS: brew install imagemagick")
        print("  • Windows: 下載安裝程式 https://imagemagick.org/script/download.php")
    
    # 檢查 Jekyll
    try:
        result = subprocess.run(['bundle', 'exec', 'jekyll', '-v'], 
                              capture_output=True, text=True)
        
        if 'jekyll' in result.stdout.lower():
            print_success(f"Jekyll 已安裝: {result.stdout.strip()}")
        else:
            print_warning("無法確認 Jekyll 安裝狀態")
    except:
        print_error("Jekyll 未安裝或無法執行")
        print("請確認已安裝 Ruby, Bundler 和 Jekyll:")
        print("  1. 安裝 Ruby")
        print("  2. gem install bundler")
        print("  3. bundle install (在網站目錄中)")

def display_help():
    """顯示說明"""
    print_header("使用說明")
    
    print("""
Loyn's Lair 圖片管理工具

這是一個整合式工具，用於管理網站的圖片和相關資料。主要功能包括:

1. 添加 Gallery 圖片
   - 添加單一圖片或批次添加多個圖片
   - 自動壓縮圖片到最適合網頁的尺寸
   - 記錄繪師、作品標題等資訊

2. 添加 Fursuit 圖片
   - 添加單一圖片或批次添加多個圖片
   - 記錄攝影師、拍攝日期等資訊

3. 建立網站
   - 使用 Jekyll 建立靜態網站

4. 啟動本地伺服器
   - 在本機預覽網站

5. 修改資料
   - 修改、刪除或重新排序現有項目

6. 修復資料檔案
   - 修復可能損壞的 YAML 或 JSON 檔案

7. 優化現有圖片
   - 重新壓縮現有圖片以節省空間

8. 匯出資料
   - 將資料匯出為 CSV, JSON 或 Markdown 格式

使用提示:
- 圖片會自動壓縮到最大寬度 1200 像素
- 資料同時以 YAML 和 JSON 格式保存，確保資料安全
- 批次模式下可以為多張圖片設置相同的作者/攝影師資訊

依賴:
- ImageMagick (用於圖片處理)
- Jekyll (用於建立網站)

若有任何問題，請創建備份後再使用本工具。
""")
    
    input("\n按 Enter 返回主選單...")

def main():
    """主選單"""
    print_header("Loyn's Lair 圖片管理工具")
    
    # 初次運行時檢查依賴
    check_dependencies()
    
    while True:
        print("\n請選擇操作:")
        print("1. 添加 Gallery 圖片")
        print("2. 添加 Fursuit 圖片")
        print("3. 建立網站")
        print("4. 啟動本地伺服器")
        print("5. 修改資料檔案")
        print("6. 修復資料檔案")
        print("7. 優化現有圖片")
        print("8. 匯出資料")
        print("9. 幫助")
        print("0. 退出")
        
        choice = input("\n請選擇 (0-9): ").strip()
        
        if choice == '1':
            add_gallery_image()
        elif choice == '2':
            add_fursuit_image()
        elif choice == '3':
            build_site()
        elif choice == '4':
            serve_site()
        elif choice == '5':
            modify_data_files()
        elif choice == '6':
            repair_data_files()
        elif choice == '7':
            optimize_existing_images()
        elif choice == '8':
            export_data()
        elif choice == '9':
            display_help()
        elif choice == '0':
            print("感謝使用，再見!")
            break
        else:
            print_error("無效選項，請重新選擇。")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已被中斷，感謝使用!")
    except Exception as e:
        print_error(f"發生未預期的錯誤: {e}")
        import traceback
        traceback.print_exc()
