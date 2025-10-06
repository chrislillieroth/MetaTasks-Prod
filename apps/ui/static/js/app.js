// Alpine.js global state and functions
function appData() {
    return {
        sidebarOpen: false,
        darkMode: false,
        loading: false,
        searchQuery: '',
        unreadNotifications: 3,
        notificationsOpen: false,
        
        init() {
            // Initialize dark mode from localStorage
            this.darkMode = localStorage.getItem('darkMode') === 'true' || 
                           (!localStorage.getItem('darkMode') && window.matchMedia('(prefers-color-scheme: dark)').matches);
            
            // Listen for system theme changes
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                if (!localStorage.getItem('darkMode')) {
                    this.darkMode = e.matches;
                }
            });
            
            // Initialize HTMX event listeners
            this.setupHTMXListeners();
            
            // Setup keyboard shortcuts
            this.setupKeyboardShortcuts();
        },
        
        toggleDarkMode() {
            this.darkMode = !this.darkMode;
            localStorage.setItem('darkMode', this.darkMode);
        },
        
        performSearch() {
            if (this.searchQuery.trim()) {
                window.location.href = `/search/?q=${encodeURIComponent(this.searchQuery)}`;
            }
        },
        
        setupHTMXListeners() {
            // Show loading state during HTMX requests
            document.body.addEventListener('htmx:beforeRequest', () => {
                this.loading = true;
            });
            
            document.body.addEventListener('htmx:afterRequest', () => {
                this.loading = false;
            });
            
            // Handle HTMX errors
            document.body.addEventListener('htmx:responseError', (event) => {
                this.showToast('Error: ' + event.detail.xhr.statusText, 'error');
            });
            
            // Handle successful responses
            document.body.addEventListener('htmx:afterSwap', (event) => {
                // Re-initialize any Alpine components in the swapped content
                if (window.Alpine) {
                    Alpine.initTree(event.target);
                }
            });
        },
        
        setupKeyboardShortcuts() {
            document.addEventListener('keydown', (e) => {
                // Cmd/Ctrl + K for search
                if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                    e.preventDefault();
                    document.querySelector('input[placeholder*="Search"]')?.focus();
                }
                
                // Cmd/Ctrl + B for sidebar toggle (mobile)
                if ((e.metaKey || e.ctrlKey) && e.key === 'b') {
                    e.preventDefault();
                    this.sidebarOpen = !this.sidebarOpen;
                }
                
                // Escape to close modals/dropdowns
                if (e.key === 'Escape') {
                    this.sidebarOpen = false;
                    this.notificationsOpen = false;
                }
            });
        },
        
        showToast(message, type = 'info', duration = 5000) {
            const toast = this.createToastElement(message, type);
            const container = document.getElementById('toast-container');
            
            if (container) {
                container.appendChild(toast);
                
                // Trigger enter animation
                setTimeout(() => {
                    toast.classList.remove('opacity-0', 'translate-x-full');
                    toast.classList.add('opacity-100', 'translate-x-0');
                }, 10);
                
                // Auto-remove after duration
                setTimeout(() => {
                    this.removeToast(toast);
                }, duration);
            }
        },
        
        createToastElement(message, type) {
            const toast = document.createElement('div');
            toast.className = `
                transform transition-all duration-300 ease-in-out opacity-0 translate-x-full
                max-w-sm w-full bg-white dark:bg-gray-800 shadow-lg rounded-lg pointer-events-auto
                ring-1 ring-black ring-opacity-5 overflow-hidden
            `;
            
            const colors = {
                success: 'text-green-500',
                error: 'text-red-500',
                warning: 'text-yellow-500',
                info: 'text-blue-500'
            };
            
            const icons = {
                success: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />`,
                error: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />`,
                warning: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />`,
                info: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />`
            };
            
            toast.innerHTML = `
                <div class="p-4">
                    <div class="flex items-start">
                        <div class="flex-shrink-0">
                            <svg class="h-6 w-6 ${colors[type] || colors.info}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                ${icons[type] || icons.info}
                            </svg>
                        </div>
                        <div class="ml-3 w-0 flex-1">
                            <p class="text-sm font-medium text-gray-900 dark:text-white">
                                ${message}
                            </p>
                        </div>
                        <div class="ml-4 flex-shrink-0 flex">
                            <button onclick="this.closest('.transform').remove()" 
                                    class="inline-flex text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            return toast;
        },
        
        removeToast(toast) {
            toast.classList.remove('opacity-100', 'translate-x-0');
            toast.classList.add('opacity-0', 'translate-x-full');
            
            setTimeout(() => {
                toast.remove();
            }, 300);
        }
    };
}

// Form validation utilities
class FormValidator {
    constructor(form) {
        this.form = form;
        this.errors = {};
    }
    
    validate(rules) {
        this.errors = {};
        const formData = new FormData(this.form);
        
        for (const [field, fieldRules] of Object.entries(rules)) {
            const value = formData.get(field);
            
            for (const rule of fieldRules) {
                if (!this.validateRule(value, rule)) {
                    if (!this.errors[field]) {
                        this.errors[field] = [];
                    }
                    this.errors[field].push(rule.message);
                }
            }
        }
        
        this.displayErrors();
        return Object.keys(this.errors).length === 0;
    }
    
    validateRule(value, rule) {
        switch (rule.type) {
            case 'required':
                return value && value.trim() !== '';
            case 'email':
                return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
            case 'min':
                return value && value.length >= rule.value;
            case 'max':
                return !value || value.length <= rule.value;
            case 'pattern':
                return !value || new RegExp(rule.value).test(value);
            default:
                return true;
        }
    }
    
    displayErrors() {
        // Clear previous errors
        this.form.querySelectorAll('.error-message').forEach(el => el.remove());
        this.form.querySelectorAll('.border-red-500').forEach(el => {
            el.classList.remove('border-red-500');
            el.classList.add('border-gray-300');
        });
        
        // Display new errors
        for (const [field, messages] of Object.entries(this.errors)) {
            const input = this.form.querySelector(`[name="${field}"]`);
            if (input) {
                input.classList.remove('border-gray-300');
                input.classList.add('border-red-500');
                
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error-message mt-1 text-sm text-red-600';
                errorDiv.textContent = messages[0];
                
                input.parentNode.insertBefore(errorDiv, input.nextSibling);
            }
        }
    }
}

// Utility functions
const Utils = {
    formatDate(date, options = {}) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            ...options
        }).format(new Date(date));
    },
    
    formatRelativeTime(date) {
        const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });
        const now = new Date();
        const target = new Date(date);
        const diff = target - now;
        
        const units = [
            { unit: 'second', ms: 1000 },
            { unit: 'minute', ms: 60 * 1000 },
            { unit: 'hour', ms: 60 * 60 * 1000 },
            { unit: 'day', ms: 24 * 60 * 60 * 1000 },
            { unit: 'week', ms: 7 * 24 * 60 * 60 * 1000 },
            { unit: 'month', ms: 30 * 24 * 60 * 60 * 1000 },
            { unit: 'year', ms: 365 * 24 * 60 * 60 * 1000 }
        ];
        
        for (let i = units.length - 1; i >= 0; i--) {
            const { unit, ms } = units[i];
            if (Math.abs(diff) >= ms) {
                return rtf.format(Math.round(diff / ms), unit);
            }
        }
        
        return rtf.format(0, 'second');
    },
    
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }
};

// Global Alpine store
document.addEventListener('alpine:init', () => {
    Alpine.store('app', {
        loading: false,
        notifications: [],
        user: null,
        
        async fetchNotifications() {
            try {
                const response = await fetch('/api/notifications/');
                const data = await response.json();
                this.notifications = data.results || [];
            } catch (error) {
                console.error('Failed to fetch notifications:', error);
            }
        },
        
        markNotificationRead(id) {
            fetch(`/api/notifications/${id}/mark-read/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json'
                }
            }).then(() => {
                this.notifications = this.notifications.filter(n => n.id !== id);
            });
        }
    });
});

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Setup CSRF token for all AJAX requests
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    if (csrfToken) {
        // For fetch requests
        window.fetch = new Proxy(window.fetch, {
            apply(target, thisArg, argumentsList) {
                const [url, options = {}] = argumentsList;
                
                if (options.method && options.method.toUpperCase() !== 'GET') {
                    options.headers = {
                        'X-CSRFToken': csrfToken,
                        ...options.headers
                    };
                }
                
                return target.apply(thisArg, [url, options]);
            }
        });
    }
    
    // Setup global error handling
    window.addEventListener('error', (event) => {
        console.error('Global error:', event.error);
        // Could send to error reporting service here
    });
    
    window.addEventListener('unhandledrejection', (event) => {
        console.error('Unhandled promise rejection:', event.reason);
        // Could send to error reporting service here
    });
});

// Export for use in other scripts
window.MetaTasks = {
    Utils,
    FormValidator,
    appData
};