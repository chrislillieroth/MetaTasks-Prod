/**
 * Analytics tracking stub for MetaTasks
 * Following specification Section 31.22 Analytics Hooks (Non-invasive)
 */

class MetaTasksAnalytics {
  constructor() {
    this.enabled = document.querySelector('[data-analytics-enabled]')?.dataset.analyticsEnabled === 'true';
    this.queue = [];
  }
  
  track(event, properties = {}) {
    if (!this.enabled) return;
    
    const payload = {
      event,
      properties: {
        ...properties,
        timestamp: new Date().toISOString(),
        url: window.location.href,
        userAgent: navigator.userAgent
      }
    };
    
    // Log to console in development
    if (this.isDevelopment()) {
      console.log('[Analytics]', payload);
    }
    
    // Queue for batch sending or send to backend
    this.queue.push(payload);
    
    // Flush queue if it gets too large
    if (this.queue.length >= 10) {
      this.flush();
    }
  }
  
  flush() {
    if (this.queue.length === 0) return;
    
    // In production, this would send to analytics backend
    // For now, we just clear the queue
    console.log(`[Analytics] Flushing ${this.queue.length} events`);
    this.queue = [];
  }
  
  isDevelopment() {
    return window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  }
}

// Initialize analytics
window.metatasks = window.metatasks || {};
window.metatasks.analytics = new MetaTasksAnalytics();

// Track page views
document.addEventListener('DOMContentLoaded', () => {
  window.metatasks.analytics.track('page_view', {
    page: document.title,
    path: window.location.pathname
  });
});

// Track clicks on elements with data-analytics attribute
document.addEventListener('click', (event) => {
  const target = event.target.closest('[data-analytics]');
  if (target) {
    const action = target.dataset.analytics;
    const properties = {};
    
    // Extract any additional data-analytics-* attributes
    Object.keys(target.dataset).forEach(key => {
      if (key.startsWith('analytics') && key !== 'analytics') {
        const propKey = key.replace('analytics', '').toLowerCase();
        properties[propKey] = target.dataset[key];
      }
    });
    
    window.metatasks.analytics.track(action, properties);
  }
});

// Track form submissions with data-analytics attribute
document.addEventListener('submit', (event) => {
  const form = event.target;
  if (form.hasAttribute('data-analytics')) {
    window.metatasks.analytics.track(form.dataset.analytics, {
      form_id: form.id,
      action: form.action
    });
  }
});

// Flush queue before page unload
window.addEventListener('beforeunload', () => {
  window.metatasks.analytics.flush();
});
