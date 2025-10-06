// MetaTasks UI JavaScript

// Toast notification system
const Toast = {
    show(message, type = 'info', duration = 5000) {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 transition-all transform ${this.getToastClasses(type)}`;
        
        toast.innerHTML = `
            <div class="p-4">
                <div class="flex items-start">
                    <div class="flex-shrink-0">
                        ${this.getIcon(type)}
                    </div>
                    <div class="ml-3 w-0 flex-1 pt-0.5">
                        <p class="text-sm font-medium ${this.getTextClass(type)}">${message}</p>
                    </div>
                    <div class="ml-4 flex flex-shrink-0">
                        <button type="button" 
                                onclick="this.closest('.pointer-events-auto').remove()" 
                                class="inline-flex rounded-md ${this.getTextClass(type)} hover:opacity-75 focus:outline-none focus:ring-2 focus:ring-offset-2">
                            <span class="sr-only">Close</span>
                            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;

        container.appendChild(toast);

        // Auto-remove after duration
        if (duration > 0) {
            setTimeout(() => {
                toast.style.opacity = '0';
                setTimeout(() => toast.remove(), 300);
            }, duration);
        }
    },

    getToastClasses(type) {
        const classes = {
            success: 'bg-green-50 dark:bg-green-900/20',
            error: 'bg-red-50 dark:bg-red-900/20',
            warning: 'bg-yellow-50 dark:bg-yellow-900/20',
            info: 'bg-blue-50 dark:bg-blue-900/20'
        };
        return classes[type] || classes.info;
    },

    getTextClass(type) {
        const classes = {
            success: 'text-green-900 dark:text-green-100',
            error: 'text-red-900 dark:text-red-100',
            warning: 'text-yellow-900 dark:text-yellow-100',
            info: 'text-blue-900 dark:text-blue-100'
        };
        return classes[type] || classes.info;
    },

    getIcon(type) {
        const icons = {
            success: '<svg class="h-6 w-6 text-green-400 dark:text-green-500" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
            error: '<svg class="h-6 w-6 text-red-400 dark:text-red-500" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
            warning: '<svg class="h-6 w-6 text-yellow-400 dark:text-yellow-500" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" /></svg>',
            info: '<svg class="h-6 w-6 text-blue-400 dark:text-blue-500" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" /></svg>'
        };
        return icons[type] || icons.info;
    }
};

// Make Toast available globally
window.Toast = Toast;

// Keyboard shortcuts
document.addEventListener('DOMContentLoaded', () => {
    // Ctrl+K to focus search
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchField = document.getElementById('search-field');
            if (searchField) {
                searchField.focus();
            }
        }
    });

    // HTMX event handlers
    document.body.addEventListener('htmx:afterSwap', (event) => {
        // You can add custom logic after HTMX swaps content
    });

    document.body.addEventListener('htmx:responseError', (event) => {
        Toast.show('An error occurred. Please try again.', 'error');
    });
});

// Form validation helper
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('border-red-500', 'dark:border-red-500');
        } else {
            input.classList.remove('border-red-500', 'dark:border-red-500');
        }
    });

    return isValid;
}

// Confirmation dialog
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Export utilities
window.validateForm = validateForm;
window.confirmAction = confirmAction;
