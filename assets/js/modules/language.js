/**
 * Language Switcher Module
 * Handles the language switching functionality for the website
 */

// Initialize the language switcher
export function initLanguageSwitcher() {
  const langButtons = document.querySelectorAll('.language-switcher .tab-link');
  
  // Add click handlers to language buttons
  langButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const lang = this.getAttribute('data-lang');
      switchLanguage(lang);
    });
  });
  
  // Set initial language based on localStorage or default to English
  const storedLang = localStorage.getItem('preferred_language') || 'en';
  switchLanguage(storedLang);
}

// Switch language display
export function switchLanguage(lang) {
  console.log('Switching language to:', lang);
  
  const langButtons = document.querySelectorAll('.language-switcher .tab-link');
  
  // Hide all language content first
  document.querySelectorAll('.lang-zh, .lang-en').forEach(el => {
    el.style.display = 'none';
  });
  
  // Remove active class from all buttons
  langButtons.forEach(btn => btn.classList.remove('active'));
  
  // Add active class to the selected language button
  const activeButton = document.querySelector(`.language-switcher .tab-link[data-lang="${lang}"]`);
  if (activeButton) {
    // Use requestAnimationFrame to ensure DOM updates and CSS transitions are in order
    requestAnimationFrame(() => {
      activeButton.classList.add('active');
    });
  }
  
  // Show content for selected language
  document.querySelectorAll(`.lang-${lang}`).forEach(el => {
    el.style.display = 'block';
  });
  
  // Fix for the tab navigation
  document.querySelectorAll('.tabs .tab-link span').forEach(span => {
    span.style.display = 'none';
  });
  
  document.querySelectorAll(`.tabs .tab-link .lang-${lang}`).forEach(span => {
    span.style.display = 'inline';
  });
  
  // Store preference
  localStorage.setItem('preferred_language', lang);
  
  // Trigger a custom event that other modules can listen for
  document.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
} 