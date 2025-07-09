/**
 * 通用工具模組
 * 提供網站中常用的輔助函數和工具
 */

/**
 * 防抖函數 - 限制函數調用頻率
 * @param {Function} func - 要防抖的函數
 * @param {number} wait - 等待時間（毫秒）
 * @returns {Function} 防抖後的函數
 */
export function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * 節流函數 - 限制函數調用頻率
 * @param {Function} func - 要節流的函數
 * @param {number} limit - 限制時間（毫秒）
 * @returns {Function} 節流後的函數
 */
export function throttle(func, limit) {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

/**
 * 檢查元素是否在視窗中可見
 * @param {Element} element - 要檢查的元素
 * @returns {boolean} 是否可見
 */
export function isElementInViewport(element) {
  const rect = element.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

/**
 * 安全地獲取元素
 * @param {string} selector - CSS 選擇器
 * @returns {Element|null} 找到的元素或 null
 */
export function safeQuerySelector(selector) {
  try {
    return document.querySelector(selector);
  } catch (error) {
    console.warn(`Invalid selector: ${selector}`, error);
    return null;
  }
}

/**
 * 安全地獲取多個元素
 * @param {string} selector - CSS 選擇器
 * @returns {NodeList|Array} 找到的元素列表
 */
export function safeQuerySelectorAll(selector) {
  try {
    return document.querySelectorAll(selector);
  } catch (error) {
    console.warn(`Invalid selector: ${selector}`, error);
    return [];
  }
}

/**
 * 添加 CSS 類別（如果不存在）
 * @param {Element} element - 目標元素
 * @param {string} className - 要添加的類別名
 */
export function addClassIfNotExists(element, className) {
  if (element && !element.classList.contains(className)) {
    element.classList.add(className);
  }
}

/**
 * 移除 CSS 類別（如果存在）
 * @param {Element} element - 目標元素
 * @param {string} className - 要移除的類別名
 */
export function removeClassIfExists(element, className) {
  if (element && element.classList.contains(className)) {
    element.classList.remove(className);
  }
}

/**
 * 切換 CSS 類別
 * @param {Element} element - 目標元素
 * @param {string} className - 要切換的類別名
 */
export function toggleClass(element, className) {
  if (element) {
    element.classList.toggle(className);
  }
}

/**
 * 檢查是否為移動設備
 * @returns {boolean} 是否為移動設備
 */
export function isMobileDevice() {
  return window.innerWidth <= 600;
}

/**
 * 檢查是否為觸控設備
 * @returns {boolean} 是否為觸控設備
 */
export function isTouchDevice() {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}

/**
 * 格式化日期
 * @param {Date|string} date - 日期對象或字符串
 * @param {string} locale - 地區設置
 * @returns {string} 格式化後的日期字符串
 */
export function formatDate(date, locale = 'zh-TW') {
  try {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    return dateObj.toLocaleDateString(locale, {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  } catch (error) {
    console.warn('Date formatting error:', error);
    return date;
  }
}

/**
 * 生成隨機 ID
 * @param {number} length - ID 長度
 * @returns {string} 隨機 ID
 */
export function generateRandomId(length = 8) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
} 