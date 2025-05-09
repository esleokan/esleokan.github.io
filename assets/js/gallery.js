// This file is being deprecated in favor of the modular approach
// Keeping it for backward compatibility

// Debounce function for optimization
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

// Handle Gallery and Fursuit page interactions
const handleGalleryInteraction = () => {
  console.log('Legacy gallery interaction handler executed - consider using the module version instead');
  
  // Import and use the new module
  import('./modules/gallery.js').then(module => {
    // Call the module's initialization function
    if (typeof module.initGalleryHandlers === 'function') {
      module.initGalleryHandlers();
    }
  }).catch(error => {
    console.error('Failed to load gallery module:', error);
    
    // Fallback to legacy implementation
    legacyGalleryImplementation();
  });
};

// Legacy implementation for fallback
function legacyGalleryImplementation() {
  const isMobile = window.innerWidth <= 600;
  
  // Use event delegation for click events
  document.addEventListener('click', (e) => {
    if (!isMobile) return;
    
    const gridItem = e.target.closest('.grid-item');
    if (gridItem) {
      // Get all other grid items in the same container
      const container = gridItem.closest('.grid, .fursuit-grid');
      if (container) {
        const items = container.querySelectorAll('.grid-item');
        items.forEach(item => {
          if (item !== gridItem) {
            item.classList.remove('overlay-active');
          }
        });
      }
      
      gridItem.classList.toggle('overlay-active');
    }
  });

  // Listen for window resize
  const handleResize = debounce(() => {
    const newIsMobile = window.innerWidth <= 600;
    if (newIsMobile !== isMobile) {
      // If switched to desktop view, remove all overlay-active classes
      if (!newIsMobile) {
        const items = document.querySelectorAll('.grid-item');
        items.forEach(item => {
          item.classList.remove('overlay-active');
        });
      }
    }
  }, 250);

  window.addEventListener('resize', handleResize);
}

// When DOM is loaded, initialize
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', handleGalleryInteraction);
} else {
  // If DOM is already loaded, execute directly
  handleGalleryInteraction();
}

// Ensure function is available globally
window.handleGalleryInteraction = handleGalleryInteraction; 