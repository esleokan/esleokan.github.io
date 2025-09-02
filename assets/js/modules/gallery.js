/**
 * Gallery Module
 * Handles the gallery and fursuit grid items interactions
 */

import { debounce } from './utils.js';

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
  
  // Setup image click handlers for gallery images with work links
  setupWorkLinkHandlers();
  
  // Setup data-link handlers
  setupDataLinkHandlers();
  
  // Use event delegation for grid items
  document.removeEventListener('click', handleGridItemClick); // Remove to prevent duplicates
  document.addEventListener('click', handleGridItemClick);
  
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
  
  window.removeEventListener('resize', handleResize); // Remove to prevent duplicates
  window.addEventListener('resize', handleResize);
}

// Setup data-link handlers
function setupDataLinkHandlers() {
  // Get all elements with data-link attribute
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
}

// Handle grid item click event
function handleGridItemClick(e) {
  const isMobile = window.innerWidth <= 600;
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
  
  // Check if clicked on an image with work-link
  if (e.target.tagName === 'IMG' && e.target.hasAttribute('data-work-link') && !e.target.closest('.grid-item').classList.contains('overlay-active')) {
    // If clicked on image with work-link and overlay is not active, show overlay first
    e.preventDefault();
    toggleOverlay(e.target.closest('.grid-item'));
    return;
  }
  
  // Handle normal grid item click
  const gridItem = e.target.closest('.grid-item');
  if (gridItem) {
    toggleOverlay(gridItem);
  }
}

// Toggle overlay visibility
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

// Setup work link handlers
function setupWorkLinkHandlers() {
  // Handle image clicks for gallery items with work links
  const galleryImagesWithWorkLinks = document.querySelectorAll('.grid .grid-item img[data-work-link]');
  galleryImagesWithWorkLinks.forEach(img => {
    img.addEventListener('dblclick', function(e) {
      const workLink = this.getAttribute('data-work-link');
      if (workLink) {
        window.open(workLink, '_blank');
      }
    });
  });
}

// Setup special gallery handlers for gallery and fursuit pages
function setupSpecialGalleryHandlers() {
  console.log('Setting up special gallery handlers');
  
  // Add any special handlers for Gallery and Fursuit pages
  // This can be extended with additional functionality
} 