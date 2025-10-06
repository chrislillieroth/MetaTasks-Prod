/**
 * WebSocket handling for real-time updates
 * Following specification Section 31.20 Real-Time UI Patterns
 */

class MetaTasksWebSocket {
  constructor() {
    this.socket = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
    this.handlers = new Map();
  }
  
  connect(url) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      return;
    }
    
    this.socket = new WebSocket(url);
    
    this.socket.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
      this.emit('connected');
    };
    
    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.handleMessage(data);
      } catch (error) {
        console.error('WebSocket message parse error:', error);
      }
    };
    
    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.emit('error', error);
    };
    
    this.socket.onclose = () => {
      console.log('WebSocket disconnected');
      this.emit('disconnected');
      this.attemptReconnect(url);
    };
  }
  
  attemptReconnect(url) {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
      
      console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
      
      setTimeout(() => {
        this.connect(url);
      }, delay);
    } else {
      console.error('Max reconnection attempts reached');
      this.emit('max_reconnect_failed');
    }
  }
  
  send(type, data) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ type, data }));
    } else {
      console.warn('WebSocket not connected');
    }
  }
  
  handleMessage(message) {
    const { type, data } = message;
    
    // Emit to registered handlers
    this.emit(type, data);
    
    // Handle common message types
    switch (type) {
      case 'workitem.updated':
        this.handleWorkItemUpdate(data);
        break;
      case 'notification':
        this.handleNotification(data);
        break;
      default:
        console.log('Unhandled message type:', type);
    }
  }
  
  handleWorkItemUpdate(data) {
    // Update work item in the UI
    const element = document.querySelector(`[data-workitem-id="${data.id}"]`);
    if (element) {
      // Trigger HTMX refresh for the element
      htmx.trigger(element, 'refresh');
    }
    
    // Show toast notification
    if (window.showToast) {
      window.showToast('info', `Work item "${data.title}" was updated`, 3000);
    }
  }
  
  handleNotification(data) {
    // Show toast notification
    if (window.showToast) {
      const type = data.level || 'info';
      window.showToast(type, data.message, 5000);
    }
    
    // Update notification badge if present
    const badge = document.querySelector('[data-notification-badge]');
    if (badge && data.unread_count !== undefined) {
      badge.textContent = data.unread_count;
      badge.classList.toggle('hidden', data.unread_count === 0);
    }
  }
  
  on(event, handler) {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, []);
    }
    this.handlers.get(event).push(handler);
  }
  
  off(event, handler) {
    if (this.handlers.has(event)) {
      const handlers = this.handlers.get(event);
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    }
  }
  
  emit(event, data) {
    if (this.handlers.has(event)) {
      this.handlers.get(event).forEach(handler => {
        try {
          handler(data);
        } catch (error) {
          console.error('Handler error:', error);
        }
      });
    }
  }
  
  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}

// Initialize WebSocket if user is authenticated
document.addEventListener('DOMContentLoaded', () => {
  const wsElement = document.querySelector('[data-websocket-url]');
  if (wsElement) {
    const wsUrl = wsElement.dataset.websocketUrl;
    window.metatasks = window.metatasks || {};
    window.metatasks.ws = new MetaTasksWebSocket();
    window.metatasks.ws.connect(wsUrl);
    
    // Clean up on page unload
    window.addEventListener('beforeunload', () => {
      window.metatasks.ws.disconnect();
    });
  }
});
