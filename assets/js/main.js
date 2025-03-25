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

