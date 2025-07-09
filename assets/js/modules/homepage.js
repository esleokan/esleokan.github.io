/**
 * 首頁專用功能模組
 * 處理 About Loyn 展開收合和頁腳顯示邏輯
 */

export function initHomepageFeatures() {
  setupLearnMoreToggle();
}

/**
 * 設置 Learn More 按鈕的展開收合功能
 */
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
      expandContent(content, arrow, footer, isHomePage);
    }
    
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      
      // 檢查內容是否隱藏
      const isHidden = content.style.display === 'none' || 
                      getComputedStyle(content).display === 'none';
      
      if (isHidden) {
        expandContent(content, arrow, footer, isHomePage);
      } else {
        collapseContent(content, arrow, footer, isHomePage);
      }
    });
  }
  
  // 如果不是首頁，確保頁腳顯示
  if (!isHomePage && footer) {
    showFooter(footer);
  }
}

/**
 * 展開內容
 */
function expandContent(content, arrow, footer, isHomePage) {
  content.style.display = 'block';
  
  if (arrow) {
    arrow.style.transform = 'rotate(180deg)';
    arrow.style.transition = 'transform 0.3s ease';
  }
  
  // 只在首頁控制頁腳顯示
  if (footer && isHomePage) {
    showFooter(footer);
  }
  
  // 保存展開狀態
  if (isHomePage) {
    localStorage.setItem('aboutLoynExpanded', 'true');
  }
}

/**
 * 收合內容
 */
function collapseContent(content, arrow, footer, isHomePage) {
  content.style.display = 'none';
  
  if (arrow) {
    arrow.style.transform = 'rotate(0deg)';
    arrow.style.transition = 'transform 0.3s ease';
  }
  
  // 只在首頁控制頁腳隱藏
  if (footer && isHomePage) {
    hideFooter(footer);
  }
  
  // 保存收合狀態
  if (isHomePage) {
    localStorage.setItem('aboutLoynExpanded', 'false');
  }
}

/**
 * 顯示頁腳
 */
function showFooter(footer) {
  footer.style.opacity = '1';
  footer.style.visibility = 'visible';
}

/**
 * 隱藏頁腳
 */
function hideFooter(footer) {
  footer.style.opacity = '0';
  footer.style.visibility = 'hidden';
} 