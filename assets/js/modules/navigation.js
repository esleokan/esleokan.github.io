/**
 * Navigation Module
 * Handles page navigation and content loading using AJAX
 */

import { switchLanguage } from './language.js';

// Initialize navigation
export function initNavigation() {
  const navTabs = document.querySelectorAll('.tabs .tab-link');
  
  // Set initial history state if not already set
  if (!history.state) {
    const currentPath = window.location.pathname;
    history.replaceState({ path: currentPath }, '', currentPath);
  }
  
  // Set initial page type class
  const pageContent = document.querySelector('#page-content');
  if (pageContent) {
    const currentPath = window.location.pathname;
    const isHomePage = currentPath === '/' || currentPath === '';
    const isGallery = currentPath.includes('/gallery');
    const isFursuit = currentPath.includes('/fursuit');
    const isPhotography = currentPath.includes('/photography');
    
    pageContent.classList.remove('home-page', 'gallery-page', 'fursuit-page', 'photography-page');
    if (isHomePage) {
      pageContent.classList.add('home-page');
    } else if (isGallery) {
      pageContent.classList.add('gallery-page');
    } else if (isFursuit) {
      pageContent.classList.add('fursuit-page');
    } else if (isPhotography) {
      pageContent.classList.add('photography-page');
    }
    
    console.log('Set initial page class for:', currentPath);
  }
  
  // Handle history state changes
  window.addEventListener('popstate', function(event) {
    console.log('popstate event', event.state, 'current path:', window.location.pathname);
    const state = event.state;
    let targetPath;
    
    if (state && state.path) {
      targetPath = state.path;
    } else {
      // Fallback to current location if no state
      targetPath = window.location.pathname;
    }
    
    console.log('Navigating to:', targetPath);
    
    // Check if we're already on the target path
    const currentPageContent = document.querySelector('#page-content');
    const isHomePage = targetPath === '/' || targetPath === '';
    const isGallery = targetPath.includes('/gallery');
    const isFursuit = targetPath.includes('/fursuit');
    const isPhotography = targetPath.includes('/photography');
    
    // Check if the current page content matches the target
    let needsReload = true;
    if (currentPageContent) {
      if (isHomePage && currentPageContent.classList.contains('home-page')) {
        needsReload = false;
      } else if (isGallery && currentPageContent.classList.contains('gallery-page')) {
        needsReload = false;
      } else if (isFursuit && currentPageContent.classList.contains('fursuit-page')) {
        needsReload = false;
      } else if (isPhotography && currentPageContent.classList.contains('photography-page')) {
        needsReload = false;
      }
    }
    
    if (needsReload) {
      loadContent(targetPath, false);
    } else {
      // Just update the active tab without reloading content
      const navTabs = document.querySelectorAll('.tabs .tab-link');
      navTabs.forEach(tab => tab.classList.remove('active'));
      
      const currentTab = document.querySelector(`.tabs .tab-link[data-path="${targetPath}"]`);
      if (currentTab) {
        currentTab.classList.add('active');
      }
      
      console.log('Content already matches, just updated tab state');
    }
  });
  
  // Add click event handlers to navigation tabs
  navTabs.forEach(tab => {
    tab.addEventListener('click', function(e) {
      console.log('Tab clicked:', this.getAttribute('data-path'));
      e.preventDefault();
      const path = this.getAttribute('data-path');
      if (path) {
        // Check if we're already on this path
        if (window.location.pathname === path) {
          console.log('Already on target path, no navigation needed');
          return;
        }
        loadContent(path);
      } else {
        console.error('No path attribute found on tab', this);
      }
    });
  });
  
  // Add SPA navigation to internal page links
  document.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (!link) return;
    
    // Skip if this is a tab link (already handled above)
    if (link.closest('.tabs')) return;
    
    const href = link.getAttribute('href');
    
    // Only handle internal page links (/, /gallery, /fursuit, /photography)
    if (href && (href === '/' || href === '/gallery' || href === '/fursuit' || href === '/photography')) {
      // Skip if it has target="_blank"
      if (link.getAttribute('target') === '_blank') return;
      
      console.log('Internal page link clicked:', href);
      e.preventDefault();
      loadContent(href);
    }
  });
}

// Load page content using AJAX
export async function loadContent(path, pushState = true) {
  console.log('Loading content for path:', path, 'pushState:', pushState);
  
  try {
    // Get current language
    const currentLang = localStorage.getItem('preferred_language') || 'zh';
    const navTabs = document.querySelectorAll('.tabs .tab-link');
    
    // Remove active state from all tabs
    navTabs.forEach(tab => tab.classList.remove('active'));
    
    // Set current page tab as active
    const currentTab = document.querySelector(`.tabs .tab-link[data-path="${path}"]`);
    if (currentTab) {
      currentTab.classList.add('active');
    }
    
    // Push state to history (for normal navigation)
    if (pushState) {
      // Only push if the path is different from current location
      if (window.location.pathname !== path) {
        history.pushState({ path: path }, '', path);
        console.log('Pushed new state:', path);
      } else {
        console.log('Skipped push state - same path:', path);
      }
    }
    
    // Don't hide the entire page, just fade the main content area
    const pageContent = document.querySelector('#page-content');
    if (pageContent) {
      // Fade out existing content (keep title visible)
      pageContent.style.opacity = '0.3';
      
      console.log('Fetching content from:', path);
      
      // Fetch new page content
      const response = await fetch(path);
      const html = await response.text();
      
      // Parse HTML
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      
      // Get new page content
      const newPageContent = doc.querySelector('#page-content');
      
      if (newPageContent) {
        console.log('New page content found, current path:', path);
        
        // Clear current page content container to avoid mixing content from multiple pages
        const isHomePage = path === '/' || path === '';
        const isGallery = path.includes('/gallery');
        const isFursuit = path.includes('/fursuit');
        const isPhotography = path.includes('/photography');
        
        // Mark current page type
        pageContent.classList.remove('home-page', 'gallery-page', 'fursuit-page', 'photography-page');
        if (isHomePage) {
          pageContent.classList.add('home-page');
        } else if (isGallery) {
          pageContent.classList.add('gallery-page');
        } else if (isFursuit) {
          pageContent.classList.add('fursuit-page');
        } else if (isPhotography) {
          pageContent.classList.add('photography-page');
        }
        
        // Replace with new page content
        pageContent.innerHTML = newPageContent.innerHTML;
        
        // Check page type to ensure correct content display
        if (isGallery) {
          // Make sure only Gallery related content is shown
          const nonGalleryContent = pageContent.querySelectorAll('.content-wrapper, .bio-section');
          nonGalleryContent.forEach(el => {
            if (el.parentNode === pageContent) {
              el.style.display = 'none';
            }
          });
          
          // Ensure Gallery content is visible
          const galleryContent = pageContent.querySelector('.grid');
          if (galleryContent) {
            galleryContent.style.display = 'block';
          }
        } else if (isFursuit) {
          // Make sure only Fursuit related content is shown
          const nonFursuitContent = pageContent.querySelectorAll('.content-wrapper, .bio-section, .grid:not(.fursuit-grid)');
          nonFursuitContent.forEach(el => {
            if (el.parentNode === pageContent) {
              el.style.display = 'none';
            }
          });
          
          // Ensure Fursuit content is visible
          const fursuitContent = pageContent.querySelector('.fursuit-grid');
          if (fursuitContent) {
            fursuitContent.style.display = 'block';
          }
        } else if (isPhotography) {
          // Make sure only Photography related content is shown
          const nonPhotographyContent = pageContent.querySelectorAll('.content-wrapper, .bio-section, .grid:not(.fursuit-grid)');
          nonPhotographyContent.forEach(el => {
            if (el.parentNode === pageContent) {
              el.style.display = 'none';
            }
          });
          
          // Ensure Photography content is visible (uses fursuit-grid class)
          const photographyContent = pageContent.querySelector('.fursuit-grid');
          if (photographyContent) {
            photographyContent.style.display = 'block';
          }
        } else if (isHomePage) {
          // Make sure only homepage related content is shown
          const galleryGrid = pageContent.querySelector('.grid:not(.fursuit-grid)');
          const fursuitGrid = pageContent.querySelector('.fursuit-grid');
          
          if (galleryGrid && galleryGrid.parentNode === pageContent) {
            galleryGrid.style.display = 'none';
          }
          
          if (fursuitGrid && fursuitGrid.parentNode === pageContent) {
            fursuitGrid.style.display = 'none';
          }
          
          // Ensure homepage content is visible
          const homeContent = pageContent.querySelector('.content-wrapper');
          const bioSection = pageContent.querySelector('.bio-section');
          
          if (homeContent) {
            homeContent.style.display = 'flex';
          }
          
          if (bioSection) {
            bioSection.style.display = 'block';
          }
        }
        
        // Fix potential image path issues
        const images = pageContent.querySelectorAll('img');
        images.forEach(img => {
          const src = img.getAttribute('src');
          if (src && src.startsWith('/') && !src.startsWith('//')) {
            // Ensure relative paths are correct
            img.setAttribute('src', src);
          }
        });
        
        console.log('Content replaced for path:', path);
        
        // Trigger custom event for page content loaded
        document.dispatchEvent(new CustomEvent('pageContentLoaded', { 
          detail: { path, pageType: isHomePage ? 'home' : isGallery ? 'gallery' : isFursuit ? 'fursuit' : isPhotography ? 'photography' : 'other' } 
        }));
        
        // Set language display
        switchLanguage(currentLang);
        
        // Scroll to top
        window.scrollTo(0, 0);
        
        // Fade in updated content
        setTimeout(() => {
          pageContent.style.opacity = '1';
        }, 100);
      } else {
        console.log('Content elements not found, redirecting');
        window.location.href = path;
      }
    } else {
      console.log('Page content element not found, redirecting');
      window.location.href = path;
    }
  } catch (error) {
    console.error('Failed to load page:', error);
    // Direct redirect on error
    window.location.href = path;
  }
} 