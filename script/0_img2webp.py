#!/usr/bin/env python3
import argparse
from PIL import Image
import os

def convert_to_webp(input_path, output_path=None, max_width=None):
    """
    將圖片轉換為 WebP 格式，可選擇性調整寬度
    
    參數:
    - input_path: 輸入圖片路徑
    - output_path: 輸出圖片路徑（可選，默認為當前目錄）
    - max_width: 最大寬度（可選，不指定則保持原始尺寸）
    """
    # 打開圖片
    img = Image.open(input_path)
    
    # 如果需要調整寬度
    if max_width and img.width > max_width:
        # 計算等比例縮放的高度
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        
        # 縮放圖片
        img = img.resize((max_width, new_height), Image.LANCZOS)
    
    # 如果沒有指定輸出路徑，使用輸入檔名但更改副檔名
    if not output_path:
        output_path = os.path.join('./', os.path.splitext(os.path.basename(input_path))[0] + '.webp')
    
    # 確保輸出目錄存在
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    # 轉換並保存為 WebP
    img.save(output_path, 'WEBP', quality=85, method=6)
    
    print(f"已轉換: {input_path} -> {output_path}")
    return output_path

def main():
    # 創建命令行解析器
    parser = argparse.ArgumentParser(description='將圖片轉換為 WebP 格式')
    
    # 添加參數
    parser.add_argument('input', help='輸入圖片路徑')
    parser.add_argument('-o', '--output', help='輸出圖片路徑（可選）')
    parser.add_argument('-w', '--width', type=int, help='最大寬度（可選）')
    
    # 解析參數
    args = parser.parse_args()
    
    # 調用轉換函數
    convert_to_webp(
        input_path=args.input, 
        output_path=args.output, 
        max_width=args.width
    )

if __name__ == "__main__":
    main()
