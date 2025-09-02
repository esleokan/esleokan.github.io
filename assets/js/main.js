/**
 * 主要 JavaScript 檔案
 * 負責初始化所有模組和處理全局功能
 */

// 導入模組化組件
import { initLanguageSwitcher, switchLanguage } from './modules/language.js';
import { initNavigation } from './modules/navigation.js';
import { initLazyLoading } from './modules/lazyLoad.js';
import { initGalleryHandlers } from './modules/gallery.js';
import { initHomepageFeatures } from './modules/homepage.js';
import { debounce, isMobileDevice } from './modules/utils.js';

/**
 * 移動選單切換功能
 * 切換導航標籤和語言切換器的顯示狀態
 */
function toggleMenu() {
  const tabMenu = document.getElementById("tabMenu");
  const langSwitcher = document.querySelector(".language-switcher");
  const menuToggle = document.querySelector(".menu-toggle");
  
  if (tabMenu) {
  tabMenu.classList.toggle("show");
  }
  
  if (langSwitcher) {
  langSwitcher.classList.toggle("show");
}

  // 更新 ARIA 狀態
  if (menuToggle) {
    const isExpanded = tabMenu && tabMenu.classList.contains("show");
    menuToggle.setAttribute("aria-expanded", isExpanded.toString());
  }
}

// 將 toggleMenu 設為全局函數，供 HTML 調用
window.toggleMenu = toggleMenu;

/**
 * 初始化響應式功能
 * 處理視窗大小變化和其他響應式行為
 */
function initResponsiveFeatures() {
  // 使用防抖處理視窗大小變化
  const handleResize = debounce(() => {
    // 在桌面版時隱藏移動選單
    if (!isMobileDevice()) {
      const tabMenu = document.getElementById("tabMenu");
      const langSwitcher = document.querySelector(".language-switcher");
      const menuToggle = document.querySelector(".menu-toggle");
      
      if (tabMenu) {
        tabMenu.classList.remove("show");
      }
      
      if (langSwitcher) {
        langSwitcher.classList.remove("show");
      }
      
      // 重置 ARIA 狀態
      if (menuToggle) {
        menuToggle.setAttribute("aria-expanded", "false");
      }
      }
  }, 250);
  
  // 監聽視窗大小變化
  window.addEventListener('resize', handleResize);
}

/**
 * 初始化頁面載入動畫
 * 確保頁面內容平滑載入
 */
function initPageLoadAnimation() {
  // 立即顯示頁面內容，避免延遲
  document.documentElement.classList.add('js-loaded');
  
  // 立即初始化關鍵模組，不使用延遲
  initAllModules();
}

/**
 * 初始化所有模組
 * 按順序初始化各個功能模組
 */
function initAllModules() {
  try {
    // 初始化語言切換器
    initLanguageSwitcher();
    
    // 初始化導航功能
    initNavigation();
    
    // 初始化畫廊處理器
    initGalleryHandlers();
    
    // 初始化懶載入
    initLazyLoading();
    
    // 初始化首頁特定功能
    initHomepageFeatures();
    
    // 初始化響應式功能
    initResponsiveFeatures();
    
    // 註冊頁面內容載入事件監聽器
    initPageContentLoadedListener();
    
    // 所有模組初始化完成
  } catch (error) {
    console.error('模組初始化錯誤:', error);
  }
}

// 頁面內容載入事件處理已整合至 core.js

/**
 * 初始化研究主題切換功能
 */
function initResearchTopicSwitcher() {
  const topicButtons = document.querySelectorAll('.topic-btn');
  const researchTopics = document.querySelectorAll('.research-topic');
  
  if (topicButtons.length === 0 || researchTopics.length === 0) {
    return;
  }
  
  topicButtons.forEach(button => {
    button.addEventListener('click', function() {
      const targetTopic = this.getAttribute('data-topic');
      
      // 移除所有按鈕的 active 類別
      topicButtons.forEach(btn => btn.classList.remove('active'));
      
      // 隱藏所有研究主題
      researchTopics.forEach(topic => {
        topic.classList.remove('active');
      });
      
      // 添加 active 類別到當前按鈕
      this.classList.add('active');
      
      // 顯示目標研究主題
      const targetElement = document.getElementById(targetTopic);
      if (targetElement) {
        // 使用 setTimeout 確保隱藏動畫完成後再顯示
        setTimeout(() => {
          targetElement.classList.add('active');
        }, 50);
      }
    });
  });
}

// 隨機排序邏輯已移至 navigation.js 模組中統一管理

/**
 * 主要初始化函數
 * 當 DOM 載入完成時執行
 */
document.addEventListener('DOMContentLoaded', function() {
  initPageLoadAnimation();
});



// 頁面可見性變化處理已簡化

