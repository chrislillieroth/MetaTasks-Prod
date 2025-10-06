/**
 * HTMX Configuration for MetaTasks
 * Following specification Section 31.9 HTMX Patterns
 */

document.addEventListener('DOMContentLoaded', function() {
  // Configure HTMX default settings
  htmx.config.globalViewTransitions = true;
  htmx.config.useTemplateFragments = true;
  
  // Default timeout for requests
  htmx.config.timeout = 30000; // 30 seconds
  
  // Add loading indicators
  document.body.addEventListener('htmx:beforeRequest', function(event) {
    const target = event.detail.target;
    if (target) {
      target.setAttribute('aria-busy', 'true');
    }
  });
  
  document.body.addEventListener('htmx:afterRequest', function(event) {
    const target = event.detail.target;
    if (target) {
      target.setAttribute('aria-busy', 'false');
    }
  });
  
  // Handle HTMX errors with toast notifications
  document.body.addEventListener('htmx:responseError', function(event) {
    const detail = event.detail;
    showToast('error', 'Request failed. Please try again.', 5000);
    console.error('HTMX Error:', detail);
  });
  
  // Success notification handler
  document.body.addEventListener('htmx:afterSwap', function(event) {
    // Check for success messages in response headers
    const successMessage = event.detail.xhr.getResponseHeader('X-Success-Message');
    if (successMessage) {
      showToast('success', successMessage, 3000);
    }
  });
  
  // Handle confirmation dialogs
  document.body.addEventListener('htmx:confirm', function(event) {
    if (event.detail.question) {
      event.preventDefault();
      if (confirm(event.detail.question)) {
        event.detail.issueRequest();
      }
    }
  });
});

/**
 * Show toast notification
 * @param {string} type - 'success', 'error', 'warning', 'info'
 * @param {string} message - The message to display
 * @param {number} duration - Duration in milliseconds (0 for persistent)
 */
function showToast(type, message, duration = 3000) {
  const container = getOrCreateToastContainer();
  
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.setAttribute('role', 'alert');
  toast.setAttribute('aria-live', 'polite');
  
  const iconMap = {
    success: `<svg class="h-5 w-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
    </svg>`,
    error: `<svg class="h-5 w-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
    </svg>`,
    warning: `<svg class="h-5 w-5 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
    </svg>`,
    info: `<svg class="h-5 w-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
    </svg>`
  };
  
  toast.innerHTML = `
    <div class="flex items-start space-x-3">
      <div class="flex-shrink-0">
        ${iconMap[type] || iconMap.info}
      </div>
      <div class="flex-1 text-sm text-gray-700 dark:text-gray-300">
        ${message}
      </div>
      <button type="button" class="flex-shrink-0 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200" onclick="this.parentElement.parentElement.remove()">
        <span class="sr-only">Close</span>
        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>
      </button>
    </div>
  `;
  
  container.appendChild(toast);
  
  if (duration > 0) {
    setTimeout(() => {
      toast.classList.add('opacity-0', 'transition-opacity');
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }
}

function getOrCreateToastContainer() {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    container.setAttribute('aria-live', 'polite');
    container.setAttribute('aria-atomic', 'true');
    document.body.appendChild(container);
  }
  return container;
}

// Expose globally for template use
window.showToast = showToast;
