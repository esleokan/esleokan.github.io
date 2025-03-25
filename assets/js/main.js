// Toggle mobile menu
function toggleMenu() {
  const tabMenu = document.getElementById("tabMenu");
  tabMenu.classList.toggle("show");
}

// Image lazy loading
document.addEventListener('DOMContentLoaded', function() {
  const images = document.querySelectorAll('.grid-item img[data-src]');
  
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        observer.unobserve(img);
      }
    });
  }, {
    rootMargin: '50px 0px', // 提前 50px 開始載入
    threshold: 0.01 // 只要 1% 進入視窗就開始載入
  });

  images.forEach(img => {
    imageObserver.observe(img);
  });
});

document.addEventListener('DOMContentLoaded', () => {
  // 處理 Gallery 網格項目
  const galleryGridItems = document.querySelectorAll('.grid .grid-item');

  galleryGridItems.forEach(item => {
    item.addEventListener('click', function(e) {
      // 如果已經有 overlay-active 類，則移除（相當於滑鼠移出）
      if (this.classList.contains('overlay-active')) {
        this.classList.remove('overlay-active');
      } else {
        // 先移除所有其他 grid-item 的 active 類
        galleryGridItems.forEach(otherItem => {
          otherItem.classList.remove('overlay-active');
        });

        // 給當前點擊的 item 添加 active 類
        this.classList.add('overlay-active');
      }
    });
  });

  // 處理 Fursuit 網格項目
  const furstuitGridItems = document.querySelectorAll('.fursuit-grid .grid-item');

  furstuitGridItems.forEach(item => {
    item.addEventListener('click', function(e) {
      // 如果已經有 overlay-active 類，則移除（相當於滑鼠移出）
      if (this.classList.contains('overlay-active')) {
        this.classList.remove('overlay-active');
      } else {
        // 先移除所有其他 grid-item 的 active 類
        furstuitGridItems.forEach(otherItem => {
          otherItem.classList.remove('overlay-active');
        });

        // 給當前點擊的 item 添加 active 類
        this.classList.add('overlay-active');
      }
    });
  });
});

