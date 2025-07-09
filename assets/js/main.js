// Import modular components
import { initLanguageSwitcher } from './modules/language.js';
import { initNavigation } from './modules/navigation.js';
import { initLazyLoading } from './modules/lazyLoad.js';
import { initGalleryHandlers } from './modules/gallery.js';

// Toggle mobile menu
function toggleMenu() {
  const tabMenu = document.getElementById("tabMenu");
  const langSwitcher = document.querySelector(".language-switcher");
  tabMenu.classList.toggle("show");
  langSwitcher.classList.toggle("show");
}

// Make toggleMenu globally available
window.toggleMenu = toggleMenu;

// Learn More toggle
function setupLearnMoreToggle() {
  const btn = document.getElementById('learn-more-btn');
  const content = document.getElementById('learn-more-content');
  const arrow = btn ? btn.querySelector('.learn-more-arrow') : null;
  const footer = document.querySelector('footer');
  
  // 檢查是否在首頁（有 learn-more-btn 的頁面）
  const isHomePage = btn !== null;
  
  // 從 localStorage 讀取保存的狀態
  const savedState = localStorage.getItem('aboutLoynExpanded');
  const wasExpanded = savedState === 'true';
  
  if (btn && content) {
    // 如果之前是展開狀態，恢復展開
    if (wasExpanded && isHomePage) {
      content.style.display = 'block';
      if (arrow) {
        arrow.style.transform = 'rotate(180deg)';
        arrow.style.transition = 'transform 0.3s ease';
      }
      if (footer) {
        footer.style.opacity = '1';
        footer.style.visibility = 'visible';
      }
    }
    
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      
      // 檢查內容是否隱藏（檢查多種可能的狀態）
      const isHidden = content.style.display === 'none' || 
                      getComputedStyle(content).display === 'none';
      
      if (isHidden) {
        // 展開內容
        content.style.display = 'block';
        if (arrow) {
          arrow.style.transform = 'rotate(180deg)';
          arrow.style.transition = 'transform 0.3s ease';
        }
        // 只在首頁控制頁腳顯示
        if (footer && isHomePage) {
          footer.style.opacity = '1';
          footer.style.visibility = 'visible';
        }
        // 保存展開狀態
        if (isHomePage) {
          localStorage.setItem('aboutLoynExpanded', 'true');
        }
      } else {
        // 收合內容
        content.style.display = 'none';
        if (arrow) {
          arrow.style.transform = 'rotate(0deg)';
          arrow.style.transition = 'transform 0.3s ease';
        }
        // 只在首頁控制頁腳隱藏
        if (footer && isHomePage) {
          footer.style.opacity = '0';
          footer.style.visibility = 'hidden';
        }
        // 保存收合狀態
        if (isHomePage) {
          localStorage.setItem('aboutLoynExpanded', 'false');
        }
      }
    });
  }
  
  // 如果不是首頁，確保頁腳顯示
  if (!isHomePage && footer) {
    footer.style.opacity = '1';
    footer.style.visibility = 'visible';
  }
}

// Main initialization function
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM content loaded');
  
  // Hide content until fully loaded
  document.body.style.visibility = 'hidden';
  
  // Initialize all modules
  requestAnimationFrame(() => {
    // Add js-loaded class
    document.documentElement.classList.add('js-loaded');
    
    // Initialize modules
    initLanguageSwitcher();
    initNavigation();
    initGalleryHandlers();
    initLazyLoading();
    setupLearnMoreToggle();
    
    // Finally show the page
    requestAnimationFrame(() => {
      document.body.style.visibility = 'visible';
    });
  });
});

document.addEventListener('pageContentLoaded', function() {
  setupLearnMoreToggle();
});

