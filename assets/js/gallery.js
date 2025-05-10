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
  
  // Setup data-link handlers
  const elementsWithDataLink = document.querySelectorAll('[data-link]');
  elementsWithDataLink.forEach(element => {
    element.style.cursor = 'pointer';
    element.classList.add('link-element');
    
    // Add click event listener
    element.addEventListener('click', function(e) {
      e.stopPropagation(); // Prevent the event from bubbling up to the grid item
      
      const linkUrl = this.getAttribute('data-link');
      if (linkUrl && linkUrl !== '#') {
        // Check if this element is inside an active overlay
        const gridItem = this.closest('.grid-item');
        const isActive = gridItem && gridItem.classList.contains('overlay-active');
        
        // Only open the link if the overlay is active
        if (isActive) {
          window.open(linkUrl, '_blank');
        } else if (window.innerWidth > 600) {
          // On desktop, it's always visible, so we can open the link
          window.open(linkUrl, '_blank');
        }
      }
    });
  });
  
  // Setup image click handlers for gallery images with work links
  const galleryImagesWithWorkLinks = document.querySelectorAll('.grid .grid-item img[data-work-link]');
  galleryImagesWithWorkLinks.forEach(img => {
    img.addEventListener('dblclick', function(e) {
      const workLink = this.getAttribute('data-work-link');
      if (workLink) {
        window.open(workLink, '_blank');
      }
    });
  });
  
  // Use event delegation for click events
  document.addEventListener('click', (e) => {
    if (!isMobile) return;
    
    // Check if clicked on an element with data-link
    if (e.target.hasAttribute('data-link') || e.target.closest('[data-link]')) {
      // If overlay is not active, activate it first
      const gridItem = e.target.closest('.grid-item');
      if (gridItem && !gridItem.classList.contains('overlay-active')) {
        e.preventDefault();
        e.stopPropagation();
        toggleOverlay(gridItem);
        return;
      }
      
      // If overlay is active, the click event will bubble up to the data-link element handler
      return;
    }
    
    // Handle images with work links
    if (e.target.tagName === 'IMG' && e.target.hasAttribute('data-work-link') && !e.target.closest('.grid-item').classList.contains('overlay-active')) {
      e.preventDefault();
      toggleOverlay(e.target.closest('.grid-item'));
      return;
    }
    
    const gridItem = e.target.closest('.grid-item');
    if (gridItem) {
      toggleOverlay(gridItem);
    }
  });

  // Helper function to toggle overlay
  function toggleOverlay(gridItem) {
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