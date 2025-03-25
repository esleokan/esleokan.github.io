#!/usr/bin/env python3
import os
import glob
from PIL import Image
import argparse

def convert_images(input_dir, output_dir=None, max_width=None, image_type='gallery'):
    """
    轉換並優化圖片
    
    :param input_dir: 輸入目錄
    :param output_dir: 輸出目錄（可選，默認為輸入目錄）
    :param max_width: 最大寬度（可選）
    :param image_type: 圖片類型 'gallery' 或 'fursuit'
    """
    # 設置默認最大寬度
    if max_width is None:
        max_width = 800 if image_type == 'gallery' else 1200

    # 如果沒有指定輸出目錄，使用輸入目錄
    if output_dir is None:
        output_dir = input_dir

    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)

    # 支持的輸入格式
    input_formats = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']

    # 收集所有圖片
    image_files = []
    for fmt in input_formats:
        image_files.extend(glob.glob(os.path.join(input_dir, fmt)))
        image_files.extend(glob.glob(os.path.join(input_dir, fmt.upper())))

    # 計數器
    total_images = 0
    converted_images = 0

    # 處理每張圖片
    for image_path in image_files:
        try:
            # 打開圖片
            img = Image.open(image_path)
            
            # 轉換為 RGB 模式以支持 WebP
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # 獲取原始尺寸
            original_width, original_height = img.size
            
            # 如果寬度大於最大寬度，進行縮放
            if original_width > max_width:
                # 計算縮放比例
                ratio = max_width / original_width
                new_height = int(original_height * ratio)
                
                # 縮放圖片
                img = img.resize((max_width, new_height), Image.LANCZOS)

            # 生成輸出路徑（固定為 WebP）
            output_filename = os.path.splitext(os.path.basename(image_path))[0] + '.webp'
            output_path = os.path.join(output_dir, output_filename)

            # 保存為 WebP
            img.save(output_path, 'WEBP', quality=85, method=6, lossless=False)

            # 如果輸出路徑與原路徑不同，刪除原文件
            if output_path != image_path:
                os.remove(image_path)

            total_images += 1
            converted_images += 1
            print(f"轉換成功: {image_path} -> {output_path}")

        except Exception as e:
            print(f"轉換失敗: {image_path}, 錯誤: {str(e)}")

    print(f"\n轉換完成！共處理 {total_images} 張圖片，成功轉換 {converted_images} 張圖片")

def main():
    # 創建命令行解析器
    parser = argparse.ArgumentParser(description='圖片轉換工具')
    
    # 添加參數
    parser.add_argument('input_dir', help='輸入目錄')
    parser.add_argument('-o', '--output_dir', help='輸出目錄（可選）')
    parser.add_argument('-t', '--type', choices=['gallery', 'fursuit'], default='gallery', help='圖片類型')
    parser.add_argument('-w', '--width', type=int, help='最大寬度（可選）')

    # 解析參數
    args = parser.parse_args()

    # 調用轉換函數
    convert_images(
        input_dir=args.input_dir, 
        output_dir=args.output_dir, 
        max_width=args.width, 
        image_type=args.type
    )

if __name__ == "__main__":
    main()
