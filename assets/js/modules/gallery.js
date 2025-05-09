/**
 * Gallery Module
 * Handles the gallery and fursuit grid items interactions
 */

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

// Initialize gallery event handlers
export function initGalleryHandlers() {
  console.log('Initializing gallery handlers');
  
  // Listen for page content loaded event
  document.addEventListener('pageContentLoaded', handlePageContentLoaded);
  
  // Initialize handlers
  setupGridHandlers();
}

// Handle page content loaded event
function handlePageContentLoaded(event) {
  const { path, pageType } = event.detail;
  console.log(`Page content loaded: ${pageType} page at path ${path}`);
  
  // Re-initialize handlers as content has changed
  setupGridHandlers();
  
  // Check if on Gallery or Fursuit page and load specific handlers
  if (pageType === 'gallery' || pageType === 'fursuit') {
    setupSpecialGalleryHandlers();
  }
}

// Setup grid items handlers
function setupGridHandlers() {
  // Handle Gallery grid items
  const galleryGridItems = document.querySelectorAll('.grid .grid-item');
  if (galleryGridItems.length > 0) {
    console.log('Found', galleryGridItems.length, 'gallery items');
  }
  
  // Handle Fursuit grid items
  const furstuitGridItems = document.querySelectorAll('.fursuit-grid .grid-item');
  if (furstuitGridItems.length > 0) {
    console.log('Found', furstuitGridItems.length, 'fursuit items');
  }
  
  // Use event delegation for grid items
  document.addEventListener('click', (e) => {
    const isMobile = window.innerWidth <= 600;
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
    const isMobile = window.innerWidth <= 600;
    if (!isMobile) {
      // If switched to desktop view, remove all overlay-active classes
      const items = document.querySelectorAll('.grid-item');
      items.forEach(item => {
        item.classList.remove('overlay-active');
      });
    }
  }, 250);
  
  window.addEventListener('resize', handleResize);
}

// Setup special gallery handlers for gallery and fursuit pages
function setupSpecialGalleryHandlers() {
  console.log('Setting up special gallery handlers');
  
  // Add any special handlers for Gallery and Fursuit pages
  // This can be extended with additional functionality
} 