// 使用事件委派和防抖優化的事件處理
const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// 使用 getElementsByClassName 優化選擇器
const handleGalleryInteraction = () => {
  const gallery = document.querySelector('.gallery-grid');
  if (!gallery) return;

  const isMobile = window.innerWidth <= 600;
  
  // 使用事件委派處理點擊事件
  gallery.addEventListener('click', (e) => {
    if (!isMobile) return;
    
    const gridItem = e.target.closest('.grid-item');
    if (gridItem) {
      gridItem.classList.toggle('overlay-active');
    }
  });

  // 監聽視窗大小改變
  const handleResize = debounce(() => {
    const newIsMobile = window.innerWidth <= 600;
    if (newIsMobile !== isMobile) {
      // 如果切換到桌面版，移除所有 overlay-active 類
      if (!newIsMobile) {
        const items = document.getElementsByClassName('grid-item');
        Array.from(items).forEach(item => {
          item.classList.remove('overlay-active');
        });
      }
    }
  }, 250);

  window.addEventListener('resize', handleResize);
};

// 當 DOM 載入完成後初始化
document.addEventListener('DOMContentLoaded', handleGalleryInteraction); 