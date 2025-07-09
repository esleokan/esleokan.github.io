/**
 * 首頁特定 JavaScript 功能
 * 包含首頁獨有的功能：About Loyn 展開收合、頁腳顯示控制
 */

import { initHomepageFeatures } from '../modules/homepage.js';

/**
 * 初始化首頁功能
 */
document.addEventListener('DOMContentLoaded', function() {
  console.log('首頁功能初始化');
  initHomepageFeatures();
});

/**
 * 頁面內容載入事件處理
 * 用於動態載入的內容
 */
document.addEventListener('pageContentLoaded', function() {
  console.log('首頁內容載入完成');
  initHomepageFeatures();
}); 