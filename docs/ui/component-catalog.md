# Component Catalog

## Overview

This document catalogs all reusable UI components in the MetaTasks application. Each component follows accessibility best practices and supports both light and dark themes.

## Base Components

### Button

**Location**: `/apps/ui/components/button.html`  
**Template Tag**: `{% render_button label variant size ... %}`

**Variants**:
- `primary` - Main call-to-action buttons
- `secondary` - Secondary actions
- `subtle` - Low-emphasis actions
- `danger` - Destructive actions
- `ghost` - Minimal style buttons

**Sizes**:
- `sm` - Small (px-3 py-1.5)
- `md` - Medium/default (px-4 py-2)
- `lg` - Large (px-6 py-3)

**Usage**:
```django
{% render_button 'Save' 'primary' 'md' icon='check' %}
{% render_button 'Cancel' 'secondary' 'md' href='/cancel/' %}
```

**Accessibility**:
- Proper focus states with ring
- Icon labels use `aria-hidden="true"`
- Disabled state uses `aria-disabled`

---

### Badge

**Template Tag**: `{% badge text status %}`  
**Filter**: `{{ status|status_badge }}`

**Status Types**:
- `success` - Green (completed, active)
- `warning` - Yellow (pending, caution)
- `danger` - Red (failed, error)
- `info` - Blue (in progress, informational)
- `neutral` - Gray (default)

**Usage**:
```django
{% badge 'Active' 'success' %}
{{ workitem.status|status_badge }}
```

---

### Modal

**Location**: `/apps/ui/components/modal.html`  
**Requires**: Alpine.js `modal()` data component

**Features**:
- Focus trap for accessibility
- Escape key to close
- Click outside to close
- Smooth transitions
- ARIA attributes

**Usage**:
```django
<div x-data="modal()">
  <button @click="show()">Open Modal</button>
  {% include 'ui/components/modal.html' with title='Confirm Action' %}
</div>
```

**Accessibility**:
- `role="dialog"` on modal container
- `aria-labelledby` for title
- Focus management with Alpine.js

---

### Alert

**Template Tag**: `{% alert message type dismissible %}`

**Types**:
- `success` - Green background
- `warning` - Yellow background
- `danger` - Red background
- `info` - Blue background

**Usage**:
```django
{% alert 'Changes saved successfully!' 'success' dismissible=True %}
```

**Accessibility**:
- `role="alert"` attribute
- Dismissible alerts have proper button labels
- Color is not the only indicator (icons used)

---

### Form Field

**Template Tag**: `{% form_field field label help_text required %}`

**Features**:
- Label with optional required indicator
- Help text support
- Error message display
- ARIA attributes for accessibility

**Usage**:
```django
{% form_field form.email label='Email Address' required=True %}
```

**Accessibility**:
- `aria-describedby` links to help text
- `aria-invalid` for errors
- Required fields marked visually and semantically

---

### Empty State

**Location**: `/apps/ui/components/empty_state.html`

**Features**:
- Icon support
- Title and description
- Optional call-to-action button

**Usage**:
```django
{% include 'ui/components/empty_state.html' with title='No items' description='Create your first item' action_label='Create' action_url='/create/' %}
```

---

### Loading Skeleton

**Location**: `/apps/ui/components/skeleton.html`

**Types**:
- `text` - Text line skeleton
- `title` - Title skeleton
- `card` - Card skeleton
- `table` - Table row skeleton
- `avatar` - Avatar skeleton

**Usage**:
```django
{% include 'ui/components/skeleton.html' with type='card' %}
```

---

### Usage Meter / Progress Bar

**Template Tag**: `{% usage_meter current limit label %}`

**Features**:
- Automatic color based on usage percentage
- Shows current/limit and percentage
- Supports unlimited limits (∞)

**Usage**:
```django
{% usage_meter 75 100 label='Work Items' %}
```

**Color Logic**:
- < 75%: Green (success)
- 75-89%: Yellow (warning)
- ≥ 90%: Red (danger)

---

### Icon

**Template Tag**: `{% icon name css_class %}`

**Available Icons**:
- `check`, `x`, `plus`, `pencil`, `trash`
- `search`, `menu`, `bell`, `cog`, `user`

**Usage**:
```django
{% icon 'check' 'w-5 h-5' %}
```

**Note**: Uses Heroicons SVG paths

---

## Layout Components

### Header

**Location**: `/apps/ui/templates/ui/partials/header.html`

**Features**:
- Brand logo and navigation
- Organization switcher dropdown
- Notifications bell
- Dark mode toggle
- User menu dropdown

---

### Sidebar

**Location**: `/apps/ui/templates/ui/partials/sidebar.html`

**Features**:
- Main navigation links
- Active state indication
- Admin section (conditional)
- Responsive (collapsible on mobile)
- Analytics tracking on links

---

### Footer

**Location**: `/apps/ui/templates/ui/partials/footer.html`

**Features**:
- Social/help links
- Copyright notice
- Privacy/Terms links

---

## Domain Components

### Work Item Row

**Location**: `/apps/ui/partials/workflows/workitem_row.html`

**Features**:
- HTMX-enabled for live updates
- Checkbox for bulk actions
- Status badge
- Assignee avatar
- Action buttons (transition, delete)

**Usage**:
```django
{% include 'ui/partials/workflows/workitem_row.html' with workitem=item %}
```

**HTMX Integration**:
- `hx-get` for details
- `hx-post` for transitions
- `hx-delete` for deletion
- `hx-target` for partial updates

---

## Error Templates

### 404 Error

**Location**: `/apps/ui/templates/ui/errors/404.html`

**Features**:
- Large error code display
- Helpful message
- Navigation options

---

### 500 Error

**Location**: `/apps/ui/templates/ui/errors/500.html`

**Features**:
- Error message
- Back navigation
- Maintains branding

---

## Component Guidelines

### Creating New Components

1. **Location**: Place in `/apps/ui/components/` for reusable components
2. **Documentation**: Add block comments explaining usage
3. **Context**: Document required context variables
4. **Accessibility**: Include ARIA attributes where needed
5. **Dark Mode**: Test in both light and dark themes
6. **Variants**: Support common variants via parameters

### Template Tag Guidelines

1. Use `@register.simple_tag` for components that return HTML
2. Use `@register.filter` for simple transformations
3. Always use `format_html()` for safety
4. Document all parameters

### Testing Components

Each component should be tested for:
- Rendering without errors
- Proper accessibility attributes
- Dark mode appearance
- Responsive behavior
- HTMX interactions (where applicable)
