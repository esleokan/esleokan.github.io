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
    
    // Finally show the page
    requestAnimationFrame(() => {
      document.body.style.visibility = 'visible';
    });
  });
});

