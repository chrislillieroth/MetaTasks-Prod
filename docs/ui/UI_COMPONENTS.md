# UI Component Library

This document provides comprehensive documentation for the MetaTasks UI component library, built with Tailwind CSS, HTMX, and Alpine.js.

## Design System

### Design Tokens

All design tokens are defined in `apps/ui/static/css/base.css` as CSS custom properties:

- **Colors**: Semantic colors (primary, secondary, accent, success, warning, danger, info)
- **Typography**: Font sizes, weights, and line heights
- **Spacing**: Modular scale based on 4px increments
- **Border Radius**: From `sm` to `full`
- **Elevation**: Shadow tokens for depth
- **Motion**: Transition durations and easing functions
- **Z-Index**: Layered stacking context

### Dark Mode

Dark mode is fully supported using the `dark:` Tailwind variant. The theme automatically adapts to:
- User's OS preference (default)
- Manual toggle via the theme switcher in the top navigation
- Preference is persisted in localStorage

## Layout Components

### Base Layout (`layouts/base.html`)

The foundational layout template with:
- **Responsive sidebar navigation** (desktop fixed, mobile overlay)
- **Top navigation bar** with search, org switcher, theme toggle, notifications, and profile menu
- **Dark mode integration** using Alpine.js
- **Toast notification container**
- **Skip to main content** link for accessibility
- **Django messages** support
- **Footer** with copyright

**Usage:**
```django
{% extends 'ui/layouts/base.html' %}

{% block title %}Page Title{% endblock %}

{% block content %}
  <!-- Your content here -->
{% endblock %}
```

## Navigation Components

### Sidebar (`partials/navigation/sidebar.html`)

Vertical navigation with:
- Logo and brand
- Primary navigation links (Dashboard, Workflows, Work Items, Calendar, Usage & Licensing)
- Admin section (conditional on permissions)
- User profile section at bottom
- Mobile close button

### Top Bar (`partials/navigation/topbar.html`)

Horizontal navigation bar featuring:
- Mobile menu button
- Global search with keyboard shortcut (`/` to focus)
- Organization switcher dropdown
- Dark mode toggle
- Notifications dropdown with badge
- Profile dropdown menu

## Core Components

### Button (`components/button.html`)

Flexible button component with multiple variants and sizes.

**Props:**
- `variant`: `primary` | `secondary` | `danger` | `success` | `ghost` | `subtle` (default: `primary`)
- `size`: `xs` | `sm` | `md` | `lg` | `xl` (default: `md`)
- `label`: Button text (required)
- `href`: URL for link buttons (optional)
- `type`: Button type for form buttons (default: `button`)
- `icon`: SVG icon markup (optional)
- `disabled`: Boolean (optional)
- `htmx_attrs`: HTMX attributes string (optional)

**Usage:**
```django
{% include 'ui/components/button.html' with variant='primary' size='md' label='Save Changes' %}
{% include 'ui/components/button.html' with variant='danger' label='Delete' icon='<path d="..."/>' %}
{% include 'ui/components/button.html' with variant='ghost' label='View Details' href='/details/' %}
```

### Badge (`components/badge.html`)

Status indicator with optional dot.

**Props:**
- `status`: `success` | `warning` | `danger` | `info` | `neutral` (required)
- `label`: Badge text (required)
- `size`: `sm` | `md` | `lg` (default: `md`)
- `dot`: Boolean to show status dot (optional)

**Usage:**
```django
{% include 'ui/components/badge.html' with status='success' label='Active' dot=True %}
{% include 'ui/components/badge.html' with status='warning' label='Pending' %}
```

### Alert (`components/alert.html`)

Contextual alert messages with icons and optional dismiss.

**Props:**
- `type`: `success` | `warning` | `danger` | `error` | `info` (required)
- `message`: Alert message text (required)
- `title`: Alert title (optional)
- `dismissible`: Boolean to allow dismissal (optional)

**Usage:**
```django
{% include 'ui/components/alert.html' with type='info' title='Notice' message='Your changes have been saved.' dismissible=True %}
{% include 'ui/components/alert.html' with type='danger' message='An error occurred.' %}
```

### Modal (`components/modal.html`)

Accessible modal dialog with backdrop and transitions.

**Props:**
- `id`: Unique modal ID (required)
- `title`: Modal title (required)
- `size`: `sm` | `md` | `lg` | `xl` (default: `md`)
- `content`: Modal body content (optional)

**Blocks:**
- `modal_content`: Custom modal body content
- `modal_footer`: Custom footer buttons

**Usage:**
```django
{% include 'ui/components/modal.html' with id='confirm-modal' title='Confirm Action' size='md' %}

{# With custom content #}
<div x-data="{ open: false }">
  {% include 'ui/components/modal.html' with id='my-modal' title='Custom Modal' %}
    {% block modal_content %}
      <p>Custom content here</p>
    {% endblock %}
    {% block modal_footer %}
      <button @click="open = false">Custom Button</button>
    {% endblock %}
  {% endinclude %}
</div>
```

### Progress/Usage Meter (`components/progress.html`)

Visual progress indicator with threshold warnings.

**Props:**
- `current`: Current value (required)
- `limit`: Maximum value (required)
- `label`: Meter label (optional)
- `show_text`: Show usage text (optional)
- `show_percentage`: Show percentage (optional)

**Features:**
- Automatic color coding: green (<70%), yellow (70-89%), red (≥90%)
- Warning messages at 70% and 90% thresholds
- Accessible with ARIA attributes

**Usage:**
```django
{% include 'ui/components/progress.html' with current=750 limit=1000 label='Work Items' show_text=True show_percentage=True %}
```

## Form Components

### Form Field (`partials/forms/field.html`)

Unified form field component supporting multiple input types.

**Props:**
- `type`: `text` | `email` | `password` | `textarea` | `select` | `checkbox` (required)
- `name`: Field name (required)
- `label`: Field label (required)
- `value`: Field value (optional)
- `placeholder`: Placeholder text (optional)
- `required`: Boolean (optional)
- `disabled`: Boolean (optional)
- `error`: Error message (optional)
- `help_text`: Help text (optional)
- `rows`: Textarea rows (default: 4)
- `options`: Array for select fields (optional)

**Usage:**
```django
{% include 'ui/partials/forms/field.html' with type='text' name='username' label='Username' required=True %}
{% include 'ui/partials/forms/field.html' with type='email' name='email' label='Email Address' placeholder='you@example.com' %}
{% include 'ui/partials/forms/field.html' with type='select' name='status' label='Status' options=status_options %}
{% include 'ui/partials/forms/field.html' with type='checkbox' name='agree' label='I agree to terms' %}
```

## State Components

### Empty State (`partials/states/empty.html`)

Display when no content is available.

**Props:**
- `title`: Empty state title (default: "No items")
- `message`: Description text (optional)
- `icon`: Custom SVG icon (optional)
- `action_url`: CTA button URL (optional)
- `action_label`: CTA button text (optional)

**Usage:**
```django
{% include 'ui/partials/states/empty.html' with title='No workflows yet' message='Get started by creating your first workflow.' action_url='/workflows/new/' action_label='Create Workflow' %}
```

### Loading State (`partials/states/loading.html`)

Display while content is loading.

**Props:**
- `type`: `spinner` | `skeleton` | `pulse` (default: `spinner`)
- `message`: Loading message (optional)

**Usage:**
```django
{% include 'ui/partials/states/loading.html' with message='Loading workflows...' %}
{% include 'ui/partials/states/loading.html' with type='skeleton' %}
{% include 'ui/partials/states/loading.html' with type='pulse' %}
```

### Error State (`partials/states/error.html`)

Display when an error occurs.

**Props:**
- `title`: Error title (default: "Error")
- `message`: Error description (optional)
- `retry_url`: Retry action URL (optional)
- `retry_label`: Retry button text (default: "Try again")

**Usage:**
```django
{% include 'ui/partials/states/error.html' with title='Failed to load' message='The workflow could not be loaded.' retry_url='/workflows/' retry_label='Back to Workflows' %}
```

## Page Examples

### Dashboard (`pages/dashboard.html`)

Full-featured dashboard demonstrating:
- Stats grid with icon cards
- License usage meter
- Alert components
- Activity timeline
- Quick actions with button variants
- Status badges
- Responsive grid layout

### Index/Landing (`pages/index.html`)

Landing page with:
- Hero section
- Feature grid with cards
- CTA buttons
- Responsive layout

## Accessibility

All components follow WCAG 2.1 AA guidelines:

- **Semantic HTML**: Proper use of `<button>`, `<nav>`, `<main>`, etc.
- **ARIA attributes**: Labels, roles, and live regions where appropriate
- **Keyboard navigation**: All interactive elements are keyboard accessible
- **Focus management**: Visible focus rings (never removed without replacement)
- **Skip links**: "Skip to main content" for screen readers
- **Color contrast**: Minimum 4.5:1 ratio for normal text
- **Alt text**: All meaningful images have alternative text

## HTMX Integration

Components support HTMX for dynamic updates:

```django
{% include 'ui/components/button.html' with 
   label='Load More' 
   htmx_attrs='hx-get="/api/items/" hx-target="#items-list" hx-swap="beforeend"' %}
```

## Alpine.js Patterns

### Dark Mode Toggle
```javascript
x-data="{ darkMode: localStorage.getItem('darkMode') === 'true' }"
@click="darkMode = !darkMode"
```

### Dropdown Menus
```javascript
x-data="{ open: false }"
@click="open = !open"
@click.away="open = false"
```

### Mobile Sidebar
```javascript
x-data="{ sidebarOpen: false }"
@click="sidebarOpen = true"
```

## Best Practices

1. **Consistency**: Always use components instead of creating one-off styles
2. **Tokens**: Use CSS variables for colors, spacing, etc. - never hardcode values
3. **Responsive**: Test all components on mobile, tablet, and desktop
4. **Dark mode**: Ensure all custom components support dark mode
5. **Accessibility**: Run manual accessibility checks and use ARIA appropriately
6. **Performance**: Use progressive enhancement - functional without JavaScript
7. **Documentation**: Document new components following this structure

## Browser Support

- Modern evergreen browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Progressive enhancement for older browsers

## Future Enhancements

Planned additions (see README.md section 31.28):
- Command palette (global fuzzy navigation)
- Toast notification system
- Visual workflow map/graph
- Skeleton loaders per component
- Automated accessibility testing in CI
