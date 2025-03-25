#!/usr/bin/env python3
import sys
import os
import yaml
import json
import shutil
import glob
import shutil
import subprocess
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageQt
import threading

# PyQt 導入
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                              QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
                              QLineEdit, QPushButton, QFileDialog, QMessageBox,
                              QListWidget, QListWidgetItem, QScrollArea, 
                              QGroupBox, QComboBox, QCheckBox, QDateEdit,
                              QProgressBar, QSplitter, QTextEdit, QSizePolicy,
                              QGridLayout, QDialog, QDialogButtonBox, QFrame)
from PySide6.QtCore import Qt, QSize, QThread, Signal, QObject, QDate, QMimeData, QUrl
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QIcon, QImage, QColor

# 設定
GALLERY_DATA_FILE = '_data/gallery.yml'
GALLERY_JSON_FILE = '_data/gallery.json'
FURSUIT_DATA_FILE = '_data/fursuit.yml'
FURSUIT_JSON_FILE = '_data/fursuit.json'
GALLERY_IMAGE_DIR = 'assets/images/gallery'
FURSUIT_IMAGE_DIR = 'assets/images/fursuit'
MAX_WIDTH = 1200
QUALITY = 85

# 確保目錄存在
for directory in [GALLERY_IMAGE_DIR, FURSUIT_IMAGE_DIR, os.path.dirname(GALLERY_DATA_FILE)]:
    os.makedirs(directory, exist_ok=True)

# 輔助函數
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
        print(f"讀取資料檔案時出錯 ({file_path}): {e}")
        return []

def save_data(data, yaml_file, json_file=None):
    """儲存資料到 YAML 和可選的 JSON 檔案"""
    try:
        # 保存為 YAML
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        
        # 如果提供了 JSON 檔案路徑，也保存為 JSON
        if json_file:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        return True
    except Exception as e:
        print(f"儲存資料檔案時出錯: {e}")
        return False

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

# 圖片處理工作線程
class ImageWorker(QThread):
    progress_signal = Signal(int, str)
    finished_signal = Signal(list)
    error_signal = Signal(str)
    
    def __init__(self, image_paths, target_dir, prefix, type_name):
        super().__init__()
        self.image_paths = image_paths
        self.target_dir = target_dir
        self.prefix = prefix
        self.type_name = type_name
        
    def run(self):
        try:
            processed_images = []
            
            # 載入相關數據
            if self.type_name == 'gallery':
                data = load_data(GALLERY_DATA_FILE)
                max_width = 800
            else:
                data = load_data(FURSUIT_DATA_FILE)
                max_width = 1200
            
            for i, image_path in enumerate(self.image_paths):
                try:
                    # 更新進度
                    progress = int((i / len(self.image_paths)) * 100)
                    self.progress_signal.emit(progress, f"處理 {os.path.basename(image_path)}...")
                    
                    # 獲取下一個編號
                    next_number = get_next_number(data, self.prefix)
                    
                    # 構建輸出路徑 (固定為 webp)
                    output_filename = f"{self.prefix}{next_number}.webp"
                    output_path = os.path.join(self.target_dir, output_filename)
                    
                    # 使用 Pillow 處理圖片
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
                    
                    # 確保目錄存在
                    os.makedirs(self.target_dir, exist_ok=True)
                    
                    # 保存圖片為 WebP 格式
                    img.save(output_path, 'WEBP', quality=QUALITY, method=6, lossless=False)
                    
                    # 將圖片信息添加到結果列表
                    web_path = f"/{self.target_dir}/{output_filename}"
                    processed_info = {
                        'original_path': image_path,
                        'processed_path': output_path,
                        'web_path': web_path,
                        'filename': output_filename
                    }
                    processed_images.append(processed_info)
                    
                except Exception as e:
                    self.error_signal.emit(f"處理圖片失敗: {os.path.basename(image_path)}, 錯誤: {str(e)}")
            
            # 完成
            self.progress_signal.emit(100, "處理完成")
            self.finished_signal.emit(processed_images)
            
        except Exception as e:
            self.error_signal.emit(f"處理中發生錯誤: {str(e)}")            
            # 完成
            self.progress_signal.emit(100, "處理完成")
            self.finished_signal.emit(processed_images)
            
        except Exception as e:
            self.error_signal.emit(f"處理中發生錯誤: {str(e)}")

# 可接受拖放的區域
class DropArea(QLabel):
    files_dropped = Signal(list)

    def __init__(self, placeholder_text="拖放圖片到這裡，或點擊選擇圖片"):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText(placeholder_text)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 8px;
                padding: 15px;
                background-color: #f8f8f8;
                min-height: 80px;  /* 減小最小高度 */
                max-height: 100px; /* 設置最大高度 */
            }
            QLabel:hover {
                background-color: #f0f0f0;
                border-color: #999;
            }
        """)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
            
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            
            # 獲取路徑
            paths = []
            for url in event.mimeData().urls():
                # 轉換為本地路徑
                path = url.toLocalFile()
                
                # 檢查是否是圖片檔案
                if path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    paths.append(path)
            
            if paths:
                self.files_dropped.emit(paths)
        else:
            event.ignore()
    
    def mousePressEvent(self, event):
        # 點擊時顯示檔案選擇對話框
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "選擇圖片",
            "",
            "圖片文件 (*.jpg *.jpeg *.png *.gif *.webp)"
        )
        
        if files:
            self.files_dropped.emit(files)

# 圖片預覽元件
class ImagePreview(QWidget):
    delete_requested = Signal(int)
    
    def __init__(self, index, image_path, parent=None):
        super().__init__(parent)
        self.index = index
        self.image_path = image_path
        
        # 創建佈局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 圖片預覽
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        
        # 載入圖片
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # 縮放圖片 (增加預覽圖尺寸)
            pixmap = pixmap.scaled(QSize(180, 180), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("圖片載入失敗")
        
        # 檔案名標籤
        self.name_label = QLabel(os.path.basename(image_path))
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        
        # 刪除按鈕
        delete_button = QPushButton("移除")
        delete_button.clicked.connect(self.request_delete)
        
        # 添加到佈局
        layout.addWidget(self.image_label)
        layout.addWidget(self.name_label)
        layout.addWidget(delete_button)
        
        # 設置樣式
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 2px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QLabel {
                padding: 2px;
            }
        """)
    
    def request_delete(self):
        self.delete_requested.emit(self.index)

# 主視窗
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loyn's Lair 圖片管理工具")
        self.setMinimumSize(900, 700)
        
        # 設置圖標
        if os.path.exists('assets/images/icon.png'):
            self.setWindowIcon(QIcon('assets/images/icon.png'))
        
        # 創建中央小部件和主佈局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # 創建標籤頁
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # 創建各頁面
        self.gallery_tab = QWidget()
        self.fursuit_tab = QWidget()
        self.tools_tab = QWidget()
        
        self.tabs.addTab(self.gallery_tab, "Gallery")
        self.tabs.addTab(self.fursuit_tab, "Fursuit")
        self.tabs.addTab(self.tools_tab, "工具")
        
        # 設置各頁面內容
        self.setup_gallery_tab()
        self.setup_fursuit_tab()
        self.setup_tools_tab()
        
        # 初始化變數
        self.gallery_images = []
        self.fursuit_images = []
        self.image_worker = None
        
        # 載入資料
        self.gallery_data = load_data(GALLERY_DATA_FILE)
        self.fursuit_data = load_data(FURSUIT_DATA_FILE)
        
        # 顯示資料數量
        self.update_status_labels()
    
    def setup_gallery_tab(self):
        """設置 Gallery 標籤頁"""
        layout = QVBoxLayout(self.gallery_tab)
        
        # 創建拖放區域 (現在更小)
        self.gallery_drop_area = DropArea("拖放 Gallery 圖片到這裡，或點擊選擇圖片")
        self.gallery_drop_area.files_dropped.connect(self.add_gallery_images)
        layout.addWidget(self.gallery_drop_area, stretch=1)  # 較小的拉伸比例
        
        # 圖片預覽區域 (現在更大)
        preview_group = QGroupBox("已選圖片")
        preview_layout = QVBoxLayout(preview_group)
        
        self.gallery_scroll_area = QScrollArea()
        self.gallery_scroll_area.setWidgetResizable(True)
        preview_layout.addWidget(self.gallery_scroll_area)
        
        self.gallery_preview_container = QWidget()
        self.gallery_preview_layout = QGridLayout(self.gallery_preview_container)
        
        self.gallery_scroll_area.setWidget(self.gallery_preview_container)
        
        # 設置預覽區域的最小高度
        preview_group.setMinimumHeight(300)  # 增加最小高度
        
        # 添加到布局，並給預覽區更大的拉伸比例
        layout.addWidget(preview_group, stretch=5)  # 更大的拉伸比例
    
        # 圖片信息輸入區
        info_group = QGroupBox("圖片資訊")
        info_layout = QFormLayout(info_group)
        
        # 輸入欄位
        self.gallery_title = QLineEdit()
        self.gallery_author = QLineEdit()
        self.gallery_author_link = QLineEdit()
        self.gallery_work_link = QLineEdit()
        
        # 批次處理選項
        self.gallery_batch_same_author = QCheckBox("所有圖片使用相同繪師")
        self.gallery_batch_same_author.toggled.connect(self.toggle_gallery_batch_fields)
        
        # 添加到表單
        info_layout.addRow("作品標題:", self.gallery_title)
        info_layout.addRow("繪師名稱:", self.gallery_author)
        info_layout.addRow("繪師連結:", self.gallery_author_link)
        info_layout.addRow("作品連結:", self.gallery_work_link)
        info_layout.addRow("批次處理:", self.gallery_batch_same_author)
        
        # 狀態標籤
        self.gallery_status_label = QLabel("Gallery 項目數: 0")
        
        # 處理按鈕
        button_layout = QHBoxLayout()
        self.gallery_process_button = QPushButton("處理並添加圖片")
        self.gallery_process_button.clicked.connect(self.process_gallery_images)
        self.gallery_process_button.setEnabled(False)
        
        self.gallery_clear_button = QPushButton("清除")
        self.gallery_clear_button.clicked.connect(self.clear_gallery_preview)
        
        button_layout.addWidget(self.gallery_process_button)
        button_layout.addWidget(self.gallery_clear_button)
        
        # 處理進度條
        self.gallery_progress_bar = QProgressBar()
        self.gallery_progress_bar.setVisible(False)
        
        # 添加到佈局
        layout.addWidget(preview_group)
        layout.addWidget(info_group)
        layout.addLayout(button_layout)
        layout.addWidget(self.gallery_progress_bar)
        layout.addWidget(self.gallery_status_label)
    
    def setup_fursuit_tab(self):
        """設置 Fursuit 標籤頁"""
        layout = QVBoxLayout(self.fursuit_tab)
        
        # 創建拖放區域 (現在更小)
        self.fursuit_drop_area = DropArea("拖放 Fursuit 圖片到這裡，或點擊選擇圖片")
        self.fursuit_drop_area.files_dropped.connect(self.add_fursuit_images)
        layout.addWidget(self.fursuit_drop_area, stretch=1)  # 較小的拉伸比例
        
        # 圖片預覽區域 (現在更大)
        preview_group = QGroupBox("已選圖片")
        preview_layout = QVBoxLayout(preview_group)
        
        self.fursuit_scroll_area = QScrollArea()
        self.fursuit_scroll_area.setWidgetResizable(True)
        preview_layout.addWidget(self.fursuit_scroll_area)
        
        self.fursuit_preview_container = QWidget()
        self.fursuit_preview_layout = QGridLayout(self.fursuit_preview_container)
        
        self.fursuit_scroll_area.setWidget(self.fursuit_preview_container)
        
        # 設置預覽區域的最小高度
        preview_group.setMinimumHeight(300)  # 增加最小高度
        
        # 添加到布局，並給預覽區更大的拉伸比例
        layout.addWidget(preview_group, stretch=5)  # 更大的拉伸比例
        
        # 圖片信息輸入區
        info_group = QGroupBox("圖片資訊")
        info_layout = QFormLayout(info_group)
        
        # 輸入欄位
        self.fursuit_title = QLineEdit()
        self.fursuit_photographer = QLineEdit()
        self.fursuit_date = QDateEdit()
        self.fursuit_date.setDate(QDate.currentDate())
        self.fursuit_description = QLineEdit()
        
        # 批次處理選項
        self.fursuit_batch_same_info = QCheckBox("所有圖片使用相同拍攝資訊")
        self.fursuit_batch_same_info.toggled.connect(self.toggle_fursuit_batch_fields)
        
        # 添加到表單
        info_layout.addRow("圖片標題:", self.fursuit_title)
        info_layout.addRow("攝影師名稱:", self.fursuit_photographer)
        info_layout.addRow("拍攝日期:", self.fursuit_date)
        info_layout.addRow("圖片描述:", self.fursuit_description)
        info_layout.addRow("批次處理:", self.fursuit_batch_same_info)
        
        # 狀態標籤
        self.fursuit_status_label = QLabel("Fursuit 項目數: 0")
        
        # 處理按鈕
        button_layout = QHBoxLayout()
        self.fursuit_process_button = QPushButton("處理並添加圖片")
        self.fursuit_process_button.clicked.connect(self.process_fursuit_images)
        self.fursuit_process_button.setEnabled(False)
        
        self.fursuit_clear_button = QPushButton("清除")
        self.fursuit_clear_button.clicked.connect(self.clear_fursuit_preview)
        
        button_layout.addWidget(self.fursuit_process_button)
        button_layout.addWidget(self.fursuit_clear_button)
        
        # 處理進度條
        self.fursuit_progress_bar = QProgressBar()
        self.fursuit_progress_bar.setVisible(False)
        
        # 添加到佈局
        layout.addWidget(preview_group)
        layout.addWidget(info_group)
        layout.addLayout(button_layout)
        layout.addWidget(self.fursuit_progress_bar)
        layout.addWidget(self.fursuit_status_label)
    
    def setup_tools_tab(self):
        """設置工具標籤頁"""
        layout = QVBoxLayout(self.tools_tab)
        
        # 站點管理工具
        site_group = QGroupBox("網站管理")
        site_layout = QVBoxLayout(site_group)
        
        build_button = QPushButton("建立網站")
        build_button.clicked.connect(self.build_site)
        
        serve_button = QPushButton("啟動本地伺服器")
        serve_button.clicked.connect(self.serve_site)
        
        site_layout.addWidget(build_button)
        site_layout.addWidget(serve_button)
        
        # 資料管理工具
        data_group = QGroupBox("資料管理")
        data_layout = QVBoxLayout(data_group)
        
        # 選擇資料類型
        data_type_layout = QHBoxLayout()
        data_type_label = QLabel("資料類型:")
        self.data_type_combo = QComboBox()
        self.data_type_combo.addItems(["Gallery", "Fursuit"])
        
        data_type_layout.addWidget(data_type_label)
        data_type_layout.addWidget(self.data_type_combo)
        
        # 功能按鈕
        view_button = QPushButton("查看資料")
        view_button.clicked.connect(self.view_data)
        
        edit_button = QPushButton("編輯資料")
        edit_button.clicked.connect(self.edit_data)
        
        export_button = QPushButton("匯出資料")
        export_button.clicked.connect(self.export_data)
        
        repair_button = QPushButton("修復資料檔案")
        repair_button.clicked.connect(self.repair_data)
        
        data_layout.addLayout(data_type_layout)
        data_layout.addWidget(view_button)
        data_layout.addWidget(edit_button)
        data_layout.addWidget(export_button)
        data_layout.addWidget(repair_button)
        
        # 圖片工具
        image_group = QGroupBox("圖片工具")
        image_layout = QVBoxLayout(image_group)
        
        optimize_button = QPushButton("優化現有圖片")
        optimize_button.clicked.connect(self.optimize_images)
        
        image_layout.addWidget(optimize_button)
        
        # 添加到主佈局
        layout.addWidget(site_group)
        layout.addWidget(data_group)
        layout.addWidget(image_group)
        
        # 添加一個擴展區域讓控件靠上排列
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(spacer)
    
    def add_gallery_images(self, file_paths):
        """添加 Gallery 圖片預覽"""
        for file_path in file_paths:
            self.gallery_images.append(file_path)
        
        self.refresh_gallery_preview()
        self.gallery_process_button.setEnabled(len(self.gallery_images) > 0)
    
    def add_fursuit_images(self, file_paths):
        """添加 Fursuit 圖片預覽"""
        for file_path in file_paths:
            self.fursuit_images.append(file_path)
        
        self.refresh_fursuit_preview()
        self.fursuit_process_button.setEnabled(len(self.fursuit_images) > 0)
    
    def refresh_gallery_preview(self):
        """刷新 Gallery 圖片預覽"""
        # 清除現有項目
        while self.gallery_preview_layout.count():
            item = self.gallery_preview_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 添加新預覽
        row, col = 0, 0
        cols = 4  # 每行顯示4張圖片
        
        for i, image_path in enumerate(self.gallery_images):
            preview = ImagePreview(i, image_path)
            preview.delete_requested.connect(self.remove_gallery_image)
            
            self.gallery_preview_layout.addWidget(preview, row, col)
            
            col += 1
            if col >= cols:
                col = 0
                row += 1
    
    def refresh_fursuit_preview(self):
        """刷新 Fursuit 圖片預覽"""
        # 清除現有項目
        while self.fursuit_preview_layout.count():
            item = self.fursuit_preview_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 添加新預覽
        row, col = 0, 0
        cols = 4  # 每行顯示4張圖片
        
        for i, image_path in enumerate(self.fursuit_images):
            preview = ImagePreview(i, image_path)
            preview.delete_requested.connect(self.remove_fursuit_image)
            
            self.fursuit_preview_layout.addWidget(preview, row, col)
            
            col += 1
            if col >= cols:
                col = 0
                row += 1
    
    def remove_gallery_image(self, index):
        """移除 Gallery 圖片"""
        if 0 <= index < len(self.gallery_images):
            self.gallery_images.pop(index)
            self.refresh_gallery_preview()
            self.gallery_process_button.setEnabled(len(self.gallery_images) > 0)
    
    def remove_fursuit_image(self, index):
        """移除 Fursuit 圖片"""
        if 0 <= index < len(self.fursuit_images):
            self.fursuit_images.pop(index)
            self.refresh_fursuit_preview()
            self.fursuit_process_button.setEnabled(len(self.fursuit_images) > 0)
    
    def clear_gallery_preview(self):
        """清除 Gallery 預覽"""
        self.gallery_images = []
        self.refresh_gallery_preview()
        self.gallery_process_button.setEnabled(False)
    
    def clear_fursuit_preview(self):
        """清除 Fursuit 預覽"""
        self.fursuit_images = []
        self.refresh_fursuit_preview()
        self.fursuit_process_button.setEnabled(False)
    
    def toggle_gallery_batch_fields(self, checked):
        """切換 Gallery 批次處理欄位狀態"""
        self.gallery_author.setEnabled(True)
        self.gallery_author_link.setEnabled(True)
        self.gallery_title.setEnabled(not checked)
        self.gallery_work_link.setEnabled(not checked)
    
    def toggle_fursuit_batch_fields(self, checked):
        """切換 Fursuit 批次處理欄位狀態"""
        self.fursuit_photographer.setEnabled(True)
        self.fursuit_date.setEnabled(True)
        self.fursuit_title.setEnabled(not checked)
        self.fursuit_description.setEnabled(not checked)
    
    def process_gallery_images(self):
        """處理 Gallery 圖片"""
        if not self.gallery_images:
            QMessageBox.warning(self, "警告", "請先選擇圖片")
            return
        
        # 禁用按鈕
        self.gallery_process_button.setEnabled(False)
        self.gallery_clear_button.setEnabled(False)
        
        # 顯示進度條
        self.gallery_progress_bar.setValue(0)
        self.gallery_progress_bar.setVisible(True)
        
        # 創建並啟動工作線程
        self.image_worker = ImageWorker(
            self.gallery_images,
            GALLERY_IMAGE_DIR,
            'loyn_comm_',
            'gallery'
        )
        
        self.image_worker.progress_signal.connect(self.update_gallery_progress)
        self.image_worker.finished_signal.connect(self.gallery_processing_finished)
        self.image_worker.error_signal.connect(self.show_error)
        
        self.image_worker.start()
    
    def process_fursuit_images(self):
        """處理 Fursuit 圖片"""
        if not self.fursuit_images:
            QMessageBox.warning(self, "警告", "請先選擇圖片")
            return
        
        # 禁用按鈕
        self.fursuit_process_button.setEnabled(False)
        self.fursuit_clear_button.setEnabled(False)
        
        # 顯示進度條
        self.fursuit_progress_bar.setValue(0)
        self.fursuit_progress_bar.setVisible(True)
        
        # 創建並啟動工作線程
        self.image_worker = ImageWorker(
            self.fursuit_images,
            FURSUIT_IMAGE_DIR,
            'loyn_fursuit_',
            'fursuit'
        )
        
        self.image_worker.progress_signal.connect(self.update_fursuit_progress)
        self.image_worker.finished_signal.connect(self.fursuit_processing_finished)
        self.image_worker.error_signal.connect(self.show_error)
        
        self.image_worker.start()
    
    def update_gallery_progress(self, value, message):
        """更新 Gallery 處理進度"""
        self.gallery_progress_bar.setValue(value)
        self.gallery_status_label.setText(message)
    
    def update_fursuit_progress(self, value, message):
        """更新 Fursuit 處理進度"""
        self.fursuit_progress_bar.setValue(value)
        self.fursuit_status_label.setText(message)
    
    def gallery_processing_finished(self, processed_images):
        """Gallery 圖片處理完成"""
        if not processed_images:
            QMessageBox.warning(self, "警告", "沒有成功處理任何圖片")
            self.gallery_progress_bar.setVisible(False)
            self.gallery_process_button.setEnabled(True)
            self.gallery_clear_button.setEnabled(True)
            return
        
        # 獲取用戶輸入的資訊
        using_batch = self.gallery_batch_same_author.isChecked()
        common_author = self.gallery_author.text().strip()
        common_author_link = self.gallery_author_link.text().strip()
        
        # 載入現有資料
        self.gallery_data = load_data(GALLERY_DATA_FILE)
        
        # 處理每個圖片
        for i, img_info in enumerate(processed_images):
            # 建立資料
            new_item = {
                'image': img_info['web_path'],
                'date_added': datetime.now().strftime('%Y-%m-%d'),
            }
            
            # 添加作者資訊
            if common_author:
                new_item['author'] = common_author
            if common_author_link:
                new_item['author_link'] = common_author_link
            
            # 如果不是批次處理相同作者，或者是處理第一張圖片
            if not using_batch or i == 0:
                title = self.gallery_title.text().strip()
                work_link = self.gallery_work_link.text().strip()
            
                if title:
                    new_item['title'] = title
                if work_link:
                    new_item['work_link'] = work_link
            
            # 如果是批次處理但不是第一張，需要輸入標題和連結
            elif using_batch and i > 0:
                # 創建對話框
                dialog = QDialog(self)
                dialog.setWindowTitle(f"圖片 {i+1} 資訊")
                
                dialog_layout = QVBoxLayout(dialog)
                
                # 顯示圖片預覽
                preview_label = QLabel()
                pixmap = QPixmap(img_info['processed_path'])
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(QSize(300, 300), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    preview_label.setPixmap(pixmap)
                
                # 輸入欄位
                form_layout = QFormLayout()
                
                title_input = QLineEdit()
                work_link_input = QLineEdit()
                
                form_layout.addRow("作品標題:", title_input)
                form_layout.addRow("作品連結:", work_link_input)
                
                # 按鈕
                buttons = QDialogButtonBox(
                    QDialogButtonBox.Ok | QDialogButtonBox.Cancel
                )
                buttons.accepted.connect(dialog.accept)
                buttons.rejected.connect(dialog.reject)
                
                # 添加到佈局
                dialog_layout.addWidget(preview_label)
                dialog_layout.addLayout(form_layout)
                dialog_layout.addWidget(buttons)
                
                # 顯示對話框
                if dialog.exec_() == QDialog.Accepted:
                    title = title_input.text().strip()
                    work_link = work_link_input.text().strip()
                    
                    if title:
                        new_item['title'] = title
                    if work_link:
                        new_item['work_link'] = work_link
                else:
                    # 用戶取消，使用默認值
                    new_item['title'] = f"Gallery 項目 {len(self.gallery_data) + 1}"
            
            # 添加到資料中
            self.gallery_data.append(new_item)
        
        # 保存資料
        if save_data(self.gallery_data, GALLERY_DATA_FILE, GALLERY_JSON_FILE):
            QMessageBox.information(
                self, 
                "成功", 
                f"已成功處理 {len(processed_images)} 張圖片並添加到 Gallery"
            )
            
            # 更新狀態
            self.update_status_labels()
            
            # 清除預覽和輸入
            self.clear_gallery_preview()
            self.gallery_title.clear()
            self.gallery_work_link.clear()
            
            # 如果批次處理被取消，也清除作者欄位
            if not using_batch:
                self.gallery_author.clear()
                self.gallery_author_link.clear()
        else:
            QMessageBox.warning(
                self, 
                "錯誤", 
                "保存資料時出錯"
            )
        
        # 重設界面
        self.gallery_progress_bar.setVisible(False)
        self.gallery_process_button.setEnabled(True)
        self.gallery_clear_button.setEnabled(True)
        self.gallery_status_label.setText(f"Gallery 項目數: {len(self.gallery_data)}")
    
    def fursuit_processing_finished(self, processed_images):
        """Fursuit 圖片處理完成"""
        if not processed_images:
            QMessageBox.warning(self, "警告", "沒有成功處理任何圖片")
            self.fursuit_progress_bar.setVisible(False)
            self.fursuit_process_button.setEnabled(True)
            self.fursuit_clear_button.setEnabled(True)
            return
        
        # 獲取用戶輸入的資訊
        using_batch = self.fursuit_batch_same_info.isChecked()
        common_photographer = self.fursuit_photographer.text().strip()
        common_date = self.fursuit_date.date().toString("yyyy-MM-dd")
        
        # 載入現有資料
        self.fursuit_data = load_data(FURSUIT_DATA_FILE)
        
        # 處理每個圖片
        for i, img_info in enumerate(processed_images):
            # 建立資料
            new_item = {
                'image': img_info['web_path'],
                'date_added': datetime.now().strftime('%Y-%m-%d'),
            }
            
            # 添加攝影師和日期資訊
            if common_photographer:
                new_item['photographer'] = common_photographer
            if common_date:
                new_item['date_taken'] = common_date
            
            # 如果不是批次處理相同資訊，或者是處理第一張圖片
            if not using_batch or i == 0:
                title = self.fursuit_title.text().strip()
                description = self.fursuit_description.text().strip()
            
                if title:
                    new_item['title'] = title
                if description:
                    new_item['description'] = description
            
            # 如果是批次處理但不是第一張，需要輸入標題和描述
            elif using_batch and i > 0:
                # 創建對話框
                dialog = QDialog(self)
                dialog.setWindowTitle(f"圖片 {i+1} 資訊")
                
                dialog_layout = QVBoxLayout(dialog)
                
                # 顯示圖片預覽
                preview_label = QLabel()
                pixmap = QPixmap(img_info['processed_path'])
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(QSize(300, 300), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    preview_label.setPixmap(pixmap)
                
                # 輸入欄位
                form_layout = QFormLayout()
                
                title_input = QLineEdit()
                description_input = QLineEdit()
                
                form_layout.addRow("圖片標題:", title_input)
                form_layout.addRow("圖片描述:", description_input)
                
                # 按鈕
                buttons = QDialogButtonBox(
                    QDialogButtonBox.Ok | QDialogButtonBox.Cancel
                )
                buttons.accepted.connect(dialog.accept)
                buttons.rejected.connect(dialog.reject)
                
                # 添加到佈局
                dialog_layout.addWidget(preview_label)
                dialog_layout.addLayout(form_layout)
                dialog_layout.addWidget(buttons)
                
                # 顯示對話框
                if dialog.exec_() == QDialog.Accepted:
                    title = title_input.text().strip()
                    description = description_input.text().strip()
                    
                    if title:
                        new_item['title'] = title
                    if description:
                        new_item['description'] = description
            
            # 添加到資料中
            self.fursuit_data.append(new_item)
        
        # 保存資料
        if save_data(self.fursuit_data, FURSUIT_DATA_FILE, FURSUIT_JSON_FILE):
            QMessageBox.information(
                self, 
                "成功", 
                f"已成功處理 {len(processed_images)} 張圖片並添加到 Fursuit"
            )
            
            # 更新狀態
            self.update_status_labels()
            
            # 清除預覽和輸入
            self.clear_fursuit_preview()
            self.fursuit_title.clear()
            self.fursuit_description.clear()
            
            # 如果批次處理被取消，也清除攝影師欄位
            if not using_batch:
                self.fursuit_photographer.clear()
        else:
            QMessageBox.warning(
                self, 
                "錯誤", 
                "保存資料時出錯"
            )
        
        # 重設界面
        self.fursuit_progress_bar.setVisible(False)
        self.fursuit_process_button.setEnabled(True)
        self.fursuit_clear_button.setEnabled(True)
        self.fursuit_status_label.setText(f"Fursuit 項目數: {len(self.fursuit_data)}")
    
    def show_error(self, message):
        """顯示錯誤訊息"""
        QMessageBox.critical(self, "錯誤", message)
    
    def update_status_labels(self):
        """更新狀態標籤"""
        self.gallery_data = load_data(GALLERY_DATA_FILE)
        self.fursuit_data = load_data(FURSUIT_DATA_FILE)
        
        self.gallery_status_label.setText(f"Gallery 項目數: {len(self.gallery_data)}")
        self.fursuit_status_label.setText(f"Fursuit 項目數: {len(self.fursuit_data)}")
    
    def build_site(self):
        """建立網站"""
        # 創建進度對話框
        progress_dialog = QDialog(self)
        progress_dialog.setWindowTitle("建立網站")
        
        dialog_layout = QVBoxLayout(progress_dialog)
        
        # 添加標籤和進度條
        status_label = QLabel("正在建立網站...")
        log_text = QTextEdit()
        log_text.setReadOnly(True)
        
        # 按鈕
        close_button = QPushButton("關閉")
        close_button.setEnabled(False)
        close_button.clicked.connect(progress_dialog.accept)
        
        # 添加到佈局
        dialog_layout.addWidget(status_label)
        dialog_layout.addWidget(log_text)
        dialog_layout.addWidget(close_button)
        
        # 顯示對話框
        progress_dialog.show()
        
        # 在工作線程中執行
        class BuildWorker(QThread):
            finished = Signal(bool, str)
            log = Signal(str)
            
            def run(self):
                try:
                    # 執行 Jekyll 建立命令
                    process = subprocess.Popen(
                        ['bundle', 'exec', 'jekyll', 'build'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    # 讀取輸出
                    for line in process.stdout:
                        self.log.emit(line.strip())
                    
                    # 等待完成
                    return_code = process.wait()
                    
                    # 檢查是否成功
                    if return_code == 0:
                        self.finished.emit(True, "網站建立成功")
                    else:
                        error = process.stderr.read()
                        self.log.emit(f"錯誤: {error}")
                        self.finished.emit(False, f"網站建立失敗 (返回碼: {return_code})")
                
                except Exception as e:
                    self.finished.emit(False, f"執行命令時出錯: {str(e)}")
        
        # 創建並啟動工作線程
        build_worker = BuildWorker()
        
        build_worker.log.connect(lambda msg: log_text.append(msg))
        build_worker.finished.connect(
            lambda success, msg: self.build_finished(success, msg, progress_dialog, close_button, status_label)
        )
        
        build_worker.start()
    
    def build_finished(self, success, message, dialog, button, label):
        """建立網站完成"""
        if success:
            label.setText("✅ " + message)
        else:
            label.setText("❌ " + message)
        
        button.setEnabled(True)
    
    def serve_site(self):
        """啟動本地伺服器"""
        # 確認是否有正在運行的伺服器
        try:
            # 查詢是否有 Jekyll 伺服器正在運行
            result = subprocess.run(
                ['lsof', '-i', ':4000'],
                capture_output=True,
                text=True
            )
            
            if 'ruby' in result.stdout or 'jekyll' in result.stdout:
                QMessageBox.warning(
                    self,
                    "警告",
                    "似乎已經有 Jekyll 伺服器在運行中。請先關閉現有伺服器。"
                )
                return
        except:
            # 如果 lsof 命令不可用，繼續嘗試啟動
            pass
        
        # 創建對話框
        serve_dialog = QDialog(self)
        serve_dialog.setWindowTitle("本地伺服器")
        serve_dialog.resize(600, 400)
        
        dialog_layout = QVBoxLayout(serve_dialog)
        
        # 添加標籤和日誌區域
        status_label = QLabel("正在啟動本地伺服器...")
        log_text = QTextEdit()
        log_text.setReadOnly(True)
        
        # URL 標籤
        url_label = QLabel("伺服器啟動後，請訪問: <a href='http://localhost:4000'>http://localhost:4000</a>")
        url_label.setOpenExternalLinks(True)
        
        # 停止按鈕
        stop_button = QPushButton("停止伺服器")
        stop_button.clicked.connect(lambda: serve_dialog.reject())
        
        # 添加到佈局
        dialog_layout.addWidget(status_label)
        dialog_layout.addWidget(url_label)
        dialog_layout.addWidget(log_text)
        dialog_layout.addWidget(stop_button)
        
        # 在工作線程中執行
        class ServeWorker(QThread):
            log = Signal(str)
            server_started = Signal()
            process = None
            
            def run(self):
                try:
                    # 執行 Jekyll 伺服器命令
                    self.process = subprocess.Popen(
                        ['bundle', 'exec', 'jekyll', 'serve'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    # 讀取輸出
                    for line in self.process.stdout:
                        self.log.emit(line.strip())
                        
                        # 檢查是否啟動成功
                        if "Server running" in line:
                            self.server_started.emit()
                    
                    # 等待完成
                    self.process.wait()
                
                except Exception as e:
                    self.log.emit(f"執行命令時出錯: {str(e)}")
            
            def stop(self):
                if self.process:
                    self.process.terminate()
        
        # 創建並啟動工作線程
        serve_worker = ServeWorker()
        
        serve_worker.log.connect(lambda msg: log_text.append(msg))
        serve_worker.server_started.connect(lambda: status_label.setText("✅ 伺服器已啟動"))
        
        serve_worker.start()
        
        # 當對話框關閉時，停止伺服器
        if serve_dialog.exec_() == QDialog.Rejected:
            serve_worker.stop()
    
    def view_data(self):
        """查看資料"""
        # 獲取選擇的資料類型
        data_type = self.data_type_combo.currentText()
        
        if data_type == "Gallery":
            data_file = GALLERY_DATA_FILE
            title = "Gallery 資料"
        else:  # Fursuit
            data_file = FURSUIT_DATA_FILE
            title = "Fursuit 資料"
        
        # 載入資料
        data = load_data(data_file)
        
        if not data:
            QMessageBox.information(self, "資訊", f"{data_type} 資料為空")
            return
        
        # 創建對話框
        view_dialog = QDialog(self)
        view_dialog.setWindowTitle(title)
        view_dialog.resize(800, 600)
        
        dialog_layout = QVBoxLayout(view_dialog)
        
        # 創建列表和詳細資訊區域
        splitter = QSplitter(Qt.Horizontal)
        
        # 左側列表
        list_widget = QListWidget()
        
        # 右側詳細資訊
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        
        # 圖片預覽
        preview_label = QLabel()
        preview_label.setAlignment(Qt.AlignCenter)
        preview_label.setMinimumHeight(200)
        
        # 詳細資訊文本
        details_text = QTextEdit()
        details_text.setReadOnly(True)
        
        details_layout.addWidget(preview_label)
        details_layout.addWidget(details_text)
        
        # 添加到分割器
        splitter.addWidget(list_widget)
        splitter.addWidget(details_widget)
        
        # 設置分割比例
        splitter.setSizes([200, 600])
        
        # 添加項目到列表
        for i, item in enumerate(data):
            title = item.get('title', f"項目 {i+1}")
            
            list_item = QListWidgetItem(title)
            list_item.setData(Qt.UserRole, i)  # 保存索引
            list_widget.addItem(list_item)
        
        # 當選擇項目時顯示詳細資訊
        def show_details(item):
            index = item.data(Qt.UserRole)
            
            if 0 <= index < len(data):
                item_data = data[index]
                
                # 顯示圖片
                image_path = item_data.get('image', '').lstrip('/')
                
                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path)
                    pixmap = pixmap.scaled(QSize(300, 300), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    preview_label.setPixmap(pixmap)
                else:
                    preview_label.setText("圖片未找到")
                
                # 顯示詳細資訊
                details = ""
                for key, value in item_data.items():
                    details += f"<b>{key}:</b> {value}<br>"
                
                details_text.setHtml(details)
        
        list_widget.itemClicked.connect(show_details)
        
        # 按鈕
        close_button = QPushButton("關閉")
        close_button.clicked.connect(view_dialog.accept)
        
        # 添加到佈局
        dialog_layout.addWidget(splitter)
        dialog_layout.addWidget(close_button)
        
        # 顯示對話框
        view_dialog.exec_()
    
    def edit_data(self):
        """編輯資料"""
        # 獲取選擇的資料類型
        data_type = self.data_type_combo.currentText()
        
        if data_type == "Gallery":
            data_file = GALLERY_DATA_FILE
            json_file = GALLERY_JSON_FILE
            title = "編輯 Gallery 資料"
        else:  # Fursuit
            data_file = FURSUIT_DATA_FILE
            json_file = FURSUIT_JSON_FILE
            title = "編輯 Fursuit 資料"
        
        # 載入資料
        data = load_data(data_file)
        
        if not data:
            QMessageBox.information(self, "資訊", f"{data_type} 資料為空")
            return
        
        # 創建對話框
        edit_dialog = QDialog(self)
        edit_dialog.setWindowTitle(title)
        edit_dialog.resize(900, 600)
        
        dialog_layout = QVBoxLayout(edit_dialog)
        
        # 創建列表和編輯區域
        splitter = QSplitter(Qt.Horizontal)
        
        # 左側列表
        list_widget = QListWidget()
        
        # 右側編輯區域
        edit_widget = QWidget()
        edit_layout = QVBoxLayout(edit_widget)
        
        # 圖片預覽
        preview_label = QLabel()
        preview_label.setAlignment(Qt.AlignCenter)
        preview_label.setMinimumHeight(200)
        
        # 表單佈局
        form_layout = QFormLayout()
        
        # 保存當前選擇的項目索引
        current_index = -1
        
        # 添加項目到列表
        for i, item in enumerate(data):
            title = item.get('title', f"項目 {i+1}")
            
            list_item = QListWidgetItem(title)
            list_item.setData(Qt.UserRole, i)  # 保存索引
            list_widget.addItem(list_item)
        
        # 更新表單的函數
        def update_form():
            # 清除現有表單
            while form_layout.rowCount() > 0:
                form_layout.removeRow(0)
            
            if current_index < 0 or current_index >= len(data):
                return
            
            item_data = data[current_index]
            
            # 顯示圖片
            image_path = item_data.get('image', '').lstrip('/')
            
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(QSize(300, 300), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                preview_label.setPixmap(pixmap)
            else:
                preview_label.setText("圖片未找到")
            
            # 為每個欄位創建輸入元件
            input_widgets = {}
            
            for key, value in item_data.items():
                if key == 'image':
                    # 圖片路徑不可編輯
                    label = QLabel(value)
                    form_layout.addRow(f"{key}:", label)
                else:
                    # 創建輸入框
                    line_edit = QLineEdit(str(value))
                    form_layout.addRow(f"{key}:", line_edit)
                    input_widgets[key] = line_edit
            
            # 添加新欄位按鈕
            add_field_button = QPushButton("添加新欄位")
            
            def add_new_field():
                field_name, ok = QInputDialog.getText(
                    edit_dialog, 
                    "添加欄位", 
                    "請輸入欄位名稱:"
                )
                
                if ok and field_name:
                    # 檢查欄位是否已存在
                    if field_name in input_widgets:
                        QMessageBox.warning(
                            edit_dialog, 
                            "警告", 
                            f"欄位 '{field_name}' 已存在"
                        )
                        return
                    
                    # 添加到表單
                    line_edit = QLineEdit()
                    form_layout.addRow(f"{field_name}:", line_edit)
                    input_widgets[field_name] = line_edit
            
            add_field_button.clicked.connect(add_new_field)
            form_layout.addRow("", add_field_button)
            
            # 保存按鈕
            save_button = QPushButton("保存更改")
            
            def save_changes():
                # 更新資料
                for key, widget in input_widgets.items():
                    data[current_index][key] = widget.text()
                
                # 更新列表項
                title = data[current_index].get('title', f"項目 {current_index+1}")
                list_widget.item(current_index).setText(title)
                
                QMessageBox.information(
                    edit_dialog, 
                    "成功", 
                    "已保存更改"
                )
            
            save_button.clicked.connect(save_changes)
            form_layout.addRow("", save_button)
            
            # 刪除按鈕
            delete_button = QPushButton("刪除項目")
            delete_button.setStyleSheet("background-color: #f44336; color: white;")
            
            def delete_item():
                confirm = QMessageBox.question(
                    edit_dialog,
                    "確認刪除",
                    "確定要刪除這個項目嗎？",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if confirm == QMessageBox.Yes:
                    # 從資料中刪除
                    data.pop(current_index)
                    
                    # 從列表中刪除
                    list_widget.takeItem(current_index)
                    
                    # 清除表單
                    while form_layout.rowCount() > 0:
                        form_layout.removeRow(0)
                    
                    preview_label.clear()
                    
                    QMessageBox.information(
                        edit_dialog, 
                        "成功", 
                        "已刪除項目"
                    )
            
            delete_button.clicked.connect(delete_item)
            form_layout.addRow("", delete_button)
        
        # 當選擇項目時顯示編輯表單
        def on_item_selected(item):
            nonlocal current_index
            current_index = item.data(Qt.UserRole)
            update_form()
        
        list_widget.itemClicked.connect(on_item_selected)
        
        # 添加表單到佈局
        edit_layout.addWidget(preview_label)
        edit_layout.addLayout(form_layout)
        
        # 添加到分割器
        splitter.addWidget(list_widget)
        splitter.addWidget(edit_widget)
        
        # 設置分割比例
        splitter.setSizes([200, 700])
        
        # 底部按鈕
        button_layout = QHBoxLayout()
        
        save_all_button = QPushButton("保存所有更改")
        cancel_button = QPushButton("取消")
        
        def save_all_changes():
            # 保存資料
            if save_data(data, data_file, json_file):
                QMessageBox.information(
                    edit_dialog,
                    "成功",
                    "所有更改已保存"
                )
                edit_dialog.accept()
            else:
                QMessageBox.warning(
                    edit_dialog,
                    "錯誤",
                    "保存資料時出錯"
                )

        save_all_button.clicked.connect(save_all_changes)
        cancel_button.clicked.connect(edit_dialog.reject)

        button_layout.addWidget(save_all_button)
        button_layout.addWidget(cancel_button)

        # 添加到佈局
        dialog_layout.addWidget(splitter)
        dialog_layout.addLayout(button_layout)

        # 顯示對話框
        if edit_dialog.exec_() == QDialog.Accepted:
            self.update_status_labels()

    def export_data(self):
        """匯出資料"""
        # 獲取選擇的資料類型
        data_type = self.data_type_combo.currentText()

        if data_type == "Gallery":
            data_file = GALLERY_DATA_FILE
        else:  # Fursuit
            data_file = FURSUIT_DATA_FILE

        # 載入資料
        data = load_data(data_file)

        if not data:
            QMessageBox.information(self, "資訊", f"{data_type} 資料為空")
            return

        # 選擇匯出格式
        format_dialog = QDialog(self)
        format_dialog.setWindowTitle("選擇匯出格式")

        dialog_layout = QVBoxLayout(format_dialog)

        # 選擇格式
        format_combo = QComboBox()
        format_combo.addItems(["CSV 格式", "JSON 格式", "Markdown 格式"])

        # 選擇路徑
        path_layout = QHBoxLayout()
        path_label = QLabel("匯出路徑:")
        path_edit = QLineEdit()
        path_button = QPushButton("瀏覽...")

        path_layout.addWidget(path_label)
        path_layout.addWidget(path_edit)
        path_layout.addWidget(path_button)

        def browse_path():
            file_path, _ = QFileDialog.getSaveFileName(
                format_dialog,
                "保存文件",
                "",
                "所有文件 (*)"
            )

            if file_path:
                path_edit.setText(file_path)

        path_button.clicked.connect(browse_path)

        # 按鈕
        button_layout = QHBoxLayout()
        export_button = QPushButton("匯出")
        cancel_button = QPushButton("取消")

        button_layout.addWidget(export_button)
        button_layout.addWidget(cancel_button)

        export_button.clicked.connect(format_dialog.accept)
        cancel_button.clicked.connect(format_dialog.reject)

        # 添加到佈局
        dialog_layout.addWidget(format_combo)
        dialog_layout.addLayout(path_layout)
        dialog_layout.addLayout(button_layout)

        # 顯示對話框
        if format_dialog.exec_() == QDialog.Accepted:
            format_index = format_combo.currentIndex()
            output_path = path_edit.text().strip()

            if not output_path:
                QMessageBox.warning(self, "警告", "請選擇匯出路徑")
                return

            # 匯出資料
            success = False

            if format_index == 0:  # CSV
                if not output_path.endswith('.csv'):
                    output_path += '.csv'

                try:
                    import csv

                    # 取得所有欄位
                    fields = set()
                    for item in data:
                        fields.update(item.keys())

                    fields = sorted(list(fields))

                    with open(output_path, 'w', encoding='utf-8', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=fields)
                        writer.writeheader()
                        writer.writerows(data)

                    success = True
                except Exception as e:
                    QMessageBox.critical(self, "錯誤", f"匯出 CSV 失敗: {str(e)}")

            elif format_index == 1:  # JSON
                if not output_path.endswith('.json'):
                    output_path += '.json'

                try:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)

                    success = True
                except Exception as e:
                    QMessageBox.critical(self, "錯誤", f"匯出 JSON 失敗: {str(e)}")

            elif format_index == 2:  # Markdown
                if not output_path.endswith('.md'):
                    output_path += '.md'

                try:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(f"# {data_type} 列表\n\n")
                        f.write(f"共 {len(data)} 個項目，生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                        for i, item in enumerate(data):
                            f.write(f"## {i+1}. ")

                            if 'title' in item and item['title']:
                                f.write(f"{item['title']}\n\n")
                            else:
                                f.write(f"無標題項目\n\n")

                            # 添加圖片
                            if 'image' in item:
                                f.write(f"![圖片]({item['image']})\n\n")

                            # 添加其他資訊
                            for key, value in item.items():
                                if key not in ['title', 'image']:
                                    f.write(f"- **{key}**: {value}\n")

                            f.write("\n---\n\n")

                    success = True
                except Exception as e:
                    QMessageBox.critical(self, "錯誤", f"匯出 Markdown 失敗: {str(e)}")

            if success:
                QMessageBox.information(
                    self,
                    "成功",
                    f"已匯出 {len(data)} 個項目至 {output_path}"
                )

    def repair_data(self):
        """修復資料檔案"""
        # 獲取選擇的資料類型
        data_type = self.data_type_combo.currentText()

        if data_type == "Gallery":
            data_file = GALLERY_DATA_FILE
            json_file = GALLERY_JSON_FILE
        else:  # Fursuit
            data_file = FURSUIT_DATA_FILE
            json_file = FURSUIT_JSON_FILE

        try:
            # 嘗試讀取 YAML
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                if not isinstance(data, list):
                    QMessageBox.warning(
                        self,
                        "警告",
                        f"{data_type} YAML 檔案格式不正確，將創建新檔案"
                    )
                    data = []
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "警告",
                    f"讀取 {data_type} YAML 檔案失敗: {str(e)}"
                )
                data = []

            # 如果 YAML 為空，嘗試從 JSON 讀取
            if not data and os.path.exists(json_file):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    if isinstance(data, list):
                        QMessageBox.information(
                            self,
                            "成功",
                            f"從 JSON 檔案恢復了 {len(data)} 個項目"
                        )
                except Exception as e:
                    QMessageBox.warning(
                        self,
                        "警告",
                        f"讀取 {data_type} JSON 檔案失敗: {str(e)}"
                    )

            # 修復每個項目
            fixed_items = []
            for item in data:
                if not isinstance(item, dict):
                    continue

                fixed_items.append(item)

            # 保存修復後的檔案
            if save_data(fixed_items, data_file, json_file):
                QMessageBox.information(
                    self,
                    "成功",
                    f"已修復 {data_type} 資料檔案，保留了 {len(fixed_items)} 個項目"
                )

                # 更新狀態
                self.update_status_labels()
            else:
                QMessageBox.critical(
                    self,
                    "錯誤",
                    f"保存 {data_type} 資料檔案失敗"
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "錯誤",
                f"修復 {data_type} 資料檔案失敗: {str(e)}"
            )

    def optimize_images(self):
        """優化現有圖片"""
        # 選擇要優化的圖片類型
        type_dialog = QDialog(self)
        type_dialog.setWindowTitle("選擇圖片類型")

        dialog_layout = QVBoxLayout(type_dialog)

        # 選擇類型
        type_combo = QComboBox()
        type_combo.addItems(["Gallery 圖片", "Fursuit 圖片", "兩者都優化"])

        # 按鈕
        button_layout = QHBoxLayout()
        ok_button = QPushButton("確定")
        cancel_button = QPushButton("取消")

        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        ok_button.clicked.connect(type_dialog.accept)
        cancel_button.clicked.connect(type_dialog.reject)

        # 添加到佈局
        dialog_layout.addWidget(QLabel("選擇要優化的圖片類型:"))
        dialog_layout.addWidget(type_combo)
        dialog_layout.addLayout(button_layout)

        # 顯示對話框
        if type_dialog.exec_() != QDialog.Accepted:
            return

        type_index = type_combo.currentIndex()

        # 創建進度對話框
        progress_dialog = QDialog(self)
        progress_dialog.setWindowTitle("優化圖片")

        progress_layout = QVBoxLayout(progress_dialog)

        # 添加標籤和進度條
        status_label = QLabel("正在掃描圖片...")
        progress_bar = QProgressBar()
        log_text = QTextEdit()
        log_text.setReadOnly(True)

        # 按鈕
        close_button = QPushButton("關閉")
        close_button.setEnabled(False)
        close_button.clicked.connect(progress_dialog.accept)

        # 添加到佈局
        progress_layout.addWidget(status_label)
        progress_layout.addWidget(progress_bar)
        progress_layout.addWidget(log_text)
        progress_layout.addWidget(close_button)

        # 顯示對話框
        progress_dialog.show()

        # 在工作線程中執行
        class OptimizeWorker(QThread):
            progress = Signal(int, str)
            log = Signal(str)
            finished = Signal()

            def __init__(self, type_index):
                super().__init__()
                self.type_index = type_index

            def run(self):
                try:
                    # 導入必要模組
                    import glob
                    import os
                    import shutil
                    from PIL import Image

                    # 根據選擇的類型確定要優化的目錄
                    directories = []

                    if self.type_index in [0, 2]:  # Gallery 或兩者
                        directories.append(GALLERY_IMAGE_DIR)

                    if self.type_index in [1, 2]:  # Fursuit 或兩者
                        directories.append(FURSUIT_IMAGE_DIR)

                    total_optimized = 0
                    total_images = 0

                    # 處理每個目錄
                    for directory in directories:
                        self.log.emit(f"處理目錄: {directory}")

                        # 檢查目錄是否存在
                        if not os.path.exists(directory):
                            self.log.emit(f"目錄不存在: {directory}")
                            continue

                        # 獲取所有圖片
                        image_files = []
                        for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']:
                            image_files.extend(glob.glob(os.path.join(directory, ext)))
                            image_files.extend(glob.glob(os.path.join(directory, ext.upper())))

                        if not image_files:
                            self.log.emit(f"在 {directory} 中找不到圖片")
                            continue

                        self.log.emit(f"找到 {len(image_files)} 張圖片")
                        total_images += len(image_files)

                        # 創建臨時目錄
                        temp_dir = os.path.join(directory, "temp_optimized")
                        os.makedirs(temp_dir, exist_ok=True)

                        # 處理每個圖片
                        for i, image_path in enumerate(image_files):
                            try:
                                # 更新進度
                                progress = int((i / len(image_files)) * 100)
                                self.progress.emit(progress, f"處理 {os.path.basename(image_path)}...")

                                filename = os.path.basename(image_path)
                                self.log.emit(f"處理圖片: {filename}")

                                # 確定目標寬度和類型
                                if directory == GALLERY_IMAGE_DIR:
                                    max_width = 800
                                    target_ext = '.webp'
                                else:
                                    max_width = 1200
                                    target_ext = '.webp'

                                # 開啟圖片
                                img = Image.open(image_path)
                                
                                # 獲取原始尺寸
                                original_width, original_height = img.size
                                original_size = os.path.getsize(image_path)

                                # 轉換為 RGB 模式以支持 WebP
                                if img.mode in ('RGBA', 'LA'):
                                    background = Image.new('RGB', img.size, (255, 255, 255))
                                    background.paste(img, mask=img.split()[-1])
                                    img = background
                                elif img.mode != 'RGB':
                                    img = img.convert('RGB')

                                # 如果寬度大於最大寬度，進行縮放
                                if original_width > max_width:
                                    # 計算縮放比例
                                    ratio = max_width / original_width
                                    new_height = int(original_height * ratio)

                                    # 縮放圖片
                                    img = img.resize((max_width, new_height), Image.LANCZOS)

                                # 臨時輸出路徑 (更改為 webp 格式)
                                base_filename = os.path.splitext(filename)[0] + target_ext
                                temp_path = os.path.join(temp_dir, base_filename)

                                # 保存圖片為 WebP 格式
                                img.save(temp_path, 'WEBP', quality=QUALITY, method=6, lossless=False)

                                # 獲取新檔案大小
                                new_size = os.path.getsize(temp_path)
                                reduction = (1 - new_size / original_size) * 100

                                if new_size < original_size:
                                    # 替換原始檔案為 WebP 格式
                                    new_image_path = os.path.splitext(image_path)[0] + '.webp'
                                    shutil.move(temp_path, new_image_path)

                                    # 如果新路徑與原路徑不同，刪除原檔案
                                    if new_image_path != image_path:
                                        try:
                                            os.remove(image_path)
                                        except:
                                            pass

                                    self.log.emit(f"  ✓ 已優化: 減少 {reduction:.1f}% ({original_size / 1024:.1f} KB -> {new_size / 1024:.1f} KB)")
                                    total_optimized += 1
                                else:
                                    # 刪除臨時檔案
                                    os.remove(temp_path)
                                    self.log.emit(f"  ✗ 優化無效果，保留原始檔案")

                            except Exception as e:
                                self.log.emit(f"  ✗ 處理圖片失敗: {str(e)}")

                        # 清理臨時目錄
                        try:
                            os.rmdir(temp_dir)
                        except:
                            pass

                    self.log.emit(f"\n優化完成! 共處理 {total_images} 張圖片，優化了 {total_optimized} 張圖片")
                    self.progress.emit(100, "優化完成")
                    self.finished.emit()

                except Exception as e:
                    self.log.emit(f"優化過程中出錯: {str(e)}")
                    self.finished.emit()

        # 創建並啟動工作線程
        optimize_worker = OptimizeWorker(type_index)

        optimize_worker.progress.connect(lambda value, msg: (progress_bar.setValue(value), status_label.setText(msg)))
        optimize_worker.log.connect(lambda msg: log_text.append(msg))
        optimize_worker.finished.connect(lambda: close_button.setEnabled(True))

        optimize_worker.start()
# 主函數
def main():
    # 檢查必要目錄
    for directory in [GALLERY_IMAGE_DIR, FURSUIT_IMAGE_DIR, os.path.dirname(GALLERY_DATA_FILE)]:
        os.makedirs(directory, exist_ok=True)

    # 運行應用程式
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
