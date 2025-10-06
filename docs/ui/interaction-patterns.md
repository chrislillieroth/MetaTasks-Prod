# Interaction Patterns

## Overview

This document describes the interaction patterns and UX conventions used throughout the MetaTasks application.

## Navigation Patterns

### Primary Navigation
- **Location**: Sidebar (authenticated users)
- **Behavior**: Active state highlighting
- **Mobile**: Collapsible via hamburger menu
- **Keyboard**: Tab navigation support

### Organization Switching
- **Trigger**: Dropdown in header
- **Behavior**: Page reload with `?org=<slug>` parameter
- **Persistence**: Stored in session middleware
- **Visual**: Shows current organization with role badge

### Breadcrumbs
- **Usage**: Complex nested pages
- **Format**: Home > Section > Page
- **Interactive**: All levels clickable except current

---

## Form Patterns

### Validation
- **Server-side first**: Primary validation on backend
- **Error display**: Below field with `aria-describedby`
- **Success feedback**: Inline messages or toast notifications
- **Field grouping**: Use `<fieldset>` + `<legend>` for related inputs

### Submission
- **Loading state**: Button disabled with spinner
- **Success**: Toast notification + redirect or inline message
- **Error**: Alert component above form or inline errors
- **Prevention**: Disable submit button during processing

### Auto-save (Future)
- **Trigger**: Debounced on input change (500ms)
- **Indicator**: "Saving..." text or spinner
- **Confirmation**: "Saved" indicator after success

---

## Modal Patterns

### Opening
- **Trigger**: Button click or HTMX response
- **Animation**: Fade in overlay + scale up content
- **Focus**: First focusable element receives focus
- **Scroll**: Body scroll locked

### Closing
- **Methods**: 
  - Close button (X)
  - Cancel button
  - Escape key
  - Click outside (overlay)
- **Animation**: Fade out + scale down
- **Focus**: Return to trigger element

### Confirmation Dialogs
- **Purpose**: Destructive actions
- **Buttons**: "Cancel" (secondary) + "Confirm" (danger)
- **Title**: Clear action description
- **Body**: Consequences explanation

**Example**:
```django
<div x-data="modal()">
  <button @click="show()" class="btn btn-danger">Delete</button>
  {% include 'ui/components/modal.html' with 
    title='Delete Work Item' 
    body='Are you sure? This action cannot be undone.' 
    confirm_label='Delete'
  %}
</div>
```

---

## Toast Notifications

### Display
- **Position**: Top-right corner (fixed)
- **Stacking**: Multiple toasts stack vertically
- **Animation**: Slide down + fade in
- **Duration**: 
  - Success: 3 seconds
  - Error: 5 seconds
  - Info: 3 seconds
  - Warning: 4 seconds

### Types
- **Success**: Green icon, dismissible
- **Error**: Red icon, dismissible
- **Warning**: Yellow icon, dismissible
- **Info**: Blue icon, dismissible

### Usage
```javascript
// Via JavaScript
showToast('success', 'Item saved successfully', 3000);

// Via HTMX header
// Server sets X-Success-Message header
```

### ARIA
- Container has `aria-live="polite"` and `aria-atomic="true"`
- Individual toasts have `role="alert"`

---

## Loading States

### Skeleton Loaders
- **When**: Initial page load or section load
- **Types**: Text, title, card, table, avatar
- **Animation**: Subtle pulse
- **Duration**: Until real content loaded

### Spinners
- **When**: Button actions, in-progress operations
- **Location**: Inline with text or centered overlay
- **Size**: Matches context (small in buttons, large in overlays)

### Progress Indicators
- **When**: Long-running operations
- **Display**: Percentage + visual bar
- **Updates**: Real-time via WebSocket or polling

---

## HTMX Interaction Patterns

### Inline Updates
- **Pattern**: Update specific element without page reload
- **Attributes**: 
  - `hx-get`: Fetch content
  - `hx-post`: Submit data
  - `hx-target`: Element to update
  - `hx-swap`: How to swap content

**Example**:
```html
<button 
  hx-post="/api/workitem/123/transition"
  hx-target="#workitem-123"
  hx-swap="outerHTML"
>
  Mark Complete
</button>
```

### Loading States
- **Indicator**: Element with class `htmx-indicator`
- **Trigger**: Shows during request
- **ARIA**: `aria-busy="true"` set automatically

### Error Handling
- **Global**: Toast notification on `htmx:responseError`
- **Inline**: Return error HTML fragment
- **Retry**: Provide retry button in error message

---

## Table Interactions

### Sorting
- **Trigger**: Click column header
- **Visual**: Arrow icon (up/down)
- **State**: Persisted in URL params

### Filtering
- **Location**: Above table or sidebar panel
- **Trigger**: Input change (debounced) or button click
- **URL**: Parameters update for bookmarkability

### Bulk Actions
- **Selection**: Checkboxes in first column
- **Actions bar**: Appears when items selected
- **Confirmation**: Modal for destructive actions

### Pagination
- **Position**: Bottom of table
- **Info**: "Showing X-Y of Z items"
- **Controls**: Previous, Next, page numbers

---

## Real-time Updates

### WebSocket Events
- **Connection**: Automatic for authenticated users
- **Reconnection**: Exponential backoff (max 5 attempts)
- **Indicators**: Connection status in UI (optional)

### Event Handling
- **Work Item Updates**: Auto-refresh affected row
- **Notifications**: Show toast + update badge
- **Presence**: User online/offline status (future)

### Optimistic Updates
- **Pattern**: Update UI immediately, rollback on error
- **Use cases**: Toggle switches, status changes
- **Error handling**: Revert + show error message

---

## Dark Mode

### Activation
- **Toggle**: Header switch (moon/sun icon)
- **Persistence**: localStorage
- **Default**: System preference via `prefers-color-scheme`

### Implementation
- **Method**: Class on `<html>` element
- **CSS**: All colors use CSS variables
- **Testing**: Both themes tested for each component

### Theme Switching
```javascript
// Alpine.js store
$store.theme.toggle()  // Toggle theme
$store.theme.dark      // Current state
```

---

## Keyboard Navigation

### Global Shortcuts (Future)
- `/` - Focus search
- `?` - Show keyboard shortcuts
- `Esc` - Close modal/dropdown
- `Ctrl+K` - Command palette

### Component Navigation
- **Modals**: Tab through focusable elements, Esc to close
- **Dropdowns**: Arrow keys to navigate, Enter to select
- **Tables**: Tab to row, Enter to activate

### Focus Management
- **Visible focus ring**: 2px blue ring with offset
- **Skip link**: "Skip to main content" at top
- **Restore focus**: After modal closes

---

## Accessibility Patterns

### Screen Reader Support
- **Landmarks**: `main`, `nav`, `aside`, `footer`
- **Headings**: Proper hierarchy (h1-h6)
- **Labels**: All form fields have labels
- **Descriptions**: `aria-describedby` for help text

### ARIA Live Regions
- **Toasts**: `aria-live="polite"`, `aria-atomic="true"`
- **Loading**: `aria-busy="true"` during HTMX requests
- **Errors**: `role="alert"` for error messages

### Color Contrast
- **Minimum**: WCAG 2.1 AA (4.5:1 for normal text)
- **Large text**: 3:1 ratio
- **Focus indicators**: 3:1 against background

### Interactive Elements
- **Target size**: Minimum 44x44px touch target
- **Spacing**: Adequate space between interactive elements
- **States**: Hover, focus, active, disabled clearly indicated

---

## Analytics Tracking

### Data Attributes
```html
<button data-analytics="workitem-transition">
  Transition
</button>
```

### Events Tracked
- Page views (automatic)
- Navigation clicks
- Form submissions
- Important actions (transitions, deletions)

### Privacy
- No personal data in events
- Respects user preferences
- Non-invasive implementation

---

## Performance Patterns

### Lazy Loading
- **Images**: `loading="lazy"` attribute
- **Components**: Load below fold on demand
- **Scripts**: Defer non-critical JavaScript

### Caching
- **Static assets**: Long cache headers
- **HTMX fragments**: Cache where appropriate
- **API responses**: ETag support

### Optimization
- **Debouncing**: Search inputs (300-500ms)
- **Throttling**: Scroll events (100ms)
- **Batch operations**: Group similar requests

---

## Error Handling UX

### Global Errors (404, 500)
- **Design**: Branded error page
- **Actions**: Home button, back button
- **Messaging**: Friendly, helpful

### Inline Errors
- **Position**: Below field or action
- **Icon**: Error icon for visual indicator
- **Action**: Retry button where applicable

### Network Errors
- **Detection**: HTMX responseError event
- **Notification**: Toast with retry option
- **Offline**: Show offline indicator

---

## Best Practices

1. **Progressive Enhancement**: Works without JavaScript
2. **Mobile First**: Design for mobile, enhance for desktop
3. **Consistency**: Reuse patterns, don't invent new ones
4. **Feedback**: Always provide feedback for user actions
5. **Accessibility**: Test with keyboard and screen reader
6. **Performance**: Monitor and optimize loading times
7. **Testing**: Test edge cases and error states
