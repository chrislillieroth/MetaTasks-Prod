/**
 * Alpine.js Initialization for MetaTasks
 * Following specification Section 31.10 Alpine.js Integration
 */

document.addEventListener('alpine:init', () => {
  // Global Alpine store for theme management
  Alpine.store('theme', {
    dark: localStorage.getItem('theme') === 'dark' || 
          (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches),
    
    toggle() {
      this.dark = !this.dark;
      this.persist();
      this.apply();
    },
    
    persist() {
      localStorage.setItem('theme', this.dark ? 'dark' : 'light');
    },
    
    apply() {
      if (this.dark) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    },
    
    init() {
      this.apply();
    }
  });
  
  // Global Alpine store for UI state
  Alpine.store('ui', {
    sidebarOpen: localStorage.getItem('sidebarOpen') === 'true',
    
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen;
      localStorage.setItem('sidebarOpen', this.sidebarOpen);
    }
  });
  
  // Modal component
  Alpine.data('modal', (open = false) => ({
    open: open,
    
    show() {
      this.open = true;
      // Focus trap - focus first focusable element
      this.$nextTick(() => {
        const focusable = this.$root.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (focusable.length) focusable[0].focus();
      });
    },
    
    close() {
      this.open = false;
    },
    
    closeOnEscape(event) {
      if (event.key === 'Escape') {
        this.close();
      }
    }
  }));
  
  // Dropdown component
  Alpine.data('dropdown', () => ({
    open: false,
    
    toggle() {
      this.open = !this.open;
    },
    
    close() {
      this.open = false;
    }
  }));
  
  // Tabs component
  Alpine.data('tabs', (defaultTab = 0) => ({
    activeTab: defaultTab,
    
    setTab(index) {
      this.activeTab = index;
    },
    
    isActive(index) {
      return this.activeTab === index;
    }
  }));
  
  // Form validation helper
  Alpine.data('formValidation', () => ({
    errors: {},
    
    setErrors(errors) {
      this.errors = errors;
    },
    
    clearError(field) {
      delete this.errors[field];
    },
    
    hasError(field) {
      return field in this.errors;
    },
    
    getError(field) {
      return this.errors[field] || '';
    }
  }));
  
  // Confirmation dialog
  Alpine.data('confirmDialog', () => ({
    open: false,
    message: '',
    callback: null,
    
    confirm(message, callback) {
      this.message = message;
      this.callback = callback;
      this.open = true;
    },
    
    proceed() {
      if (this.callback) {
        this.callback();
      }
      this.close();
    },
    
    close() {
      this.open = false;
      this.message = '';
      this.callback = null;
    }
  }));
});

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', () => {
  // Initialize Alpine store
  if (window.Alpine && Alpine.store('theme')) {
    Alpine.store('theme').init();
  }
});
