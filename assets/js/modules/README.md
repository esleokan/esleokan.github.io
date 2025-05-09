# JavaScript Module Structure

This directory contains the modular JavaScript code for the blog. The code has been restructured to improve maintainability, readability, and performance.

## Module Overview

- **main.js**: The main entry point that imports and initializes all modules
- **language.js**: Handles language switching functionality 
- **navigation.js**: Manages page navigation and AJAX content loading
- **gallery.js**: Handles gallery and fursuit grid interactions
- **lazyLoad.js**: Implements lazy loading for images

## Architecture

The code uses ES modules and follows a modular pattern to separate concerns and make the codebase easier to maintain. Each module is responsible for a specific functionality:

### Language Module
- Manages the language switcher UI
- Stores and retrieves language preferences from localStorage
- Ensures correct content display based on selected language

### Navigation Module
- Handles AJAX-based page navigation
- Manages browser history state
- Ensures smooth transitions between pages

### Gallery Module
- Handles interactions with gallery and fursuit grid items
- Implements mobile-specific touch interactions
- Uses event delegation for better performance

### Lazy Loading Module
- Implements image lazy loading using IntersectionObserver
- Optimizes page load performance

## Event System

The modules communicate using custom events:
- `languageChanged`: Triggered when language is switched
- `pageContentLoaded`: Triggered when new page content is loaded

## Upgrading
The old implementation is being phased out in favor of this modular approach. The original files are kept for backward compatibility but will redirect to the new modules when possible. 