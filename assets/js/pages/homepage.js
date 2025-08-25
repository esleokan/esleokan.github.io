/**
 * 首頁特定 JavaScript 功能
 * 包含首頁獨有的功能
 */

import { initHomepageFeatures } from '../modules/homepage.js';

/**
 * 初始化首頁功能
 */
// 使用更高效的事件監聽器，避免延遲
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initHomepageFeatures);
} else {
  // 如果 DOM 已經載入完成，立即執行
  initHomepageFeatures();
} 