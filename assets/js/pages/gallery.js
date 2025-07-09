/**
 * 畫廊頁面特定 JavaScript 功能
 * 包含畫廊、獸裝、攝影頁面的功能：圖片處理、懶載入、隨機排序
 */

import { initGalleryHandlers } from '../modules/gallery.js';
import { initLazyLoading } from '../modules/lazyLoad.js';

/**
 * 初始化畫廊功能
 */
document.addEventListener('DOMContentLoaded', function() {
  console.log('畫廊功能初始化');
  
  // 初始化畫廊處理器
  initGalleryHandlers();
  
  // 初始化懶載入
  initLazyLoading();
}); 