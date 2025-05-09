/**
 * Lazy Loading Module
 * Handles lazy loading of images for better performance
 */

// Initialize lazy loading
export function initLazyLoading() {
  console.log('Initializing lazy loading');
  
  // Listen for page content loaded event to reinitialize lazy loading
  document.addEventListener('pageContentLoaded', () => {
    setupLazyLoading();
  });
  
  // Initial setup
  setupLazyLoading();
}

// Setup lazy loading for images
function setupLazyLoading() {
  // Look for all images with data-src attribute
  const images = document.querySelectorAll('img[data-src]');
  
  if (images.length > 0) {
    console.log('Setting up lazy loading for', images.length, 'images');
    
    // Use Intersection Observer to detect when images enter viewport
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
      rootMargin: '50px 0px', // Start loading 50px before entering viewport
      threshold: 0.01 // Trigger when at least 1% of the image is visible
    });
    
    // Observe each image
    images.forEach(img => {
      imageObserver.observe(img);
    });
  }
} 