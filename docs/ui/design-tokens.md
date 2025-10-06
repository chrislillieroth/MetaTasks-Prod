# Design Tokens Documentation

## Overview

MetaTasks uses a token-based design system to ensure consistency across the UI. All design tokens are defined as CSS variables in `/apps/ui/static/css/base.css`.

## Color Palette

### Primary Colors
- `--color-primary: #3b82f6` - Main brand color (blue-600)
- `--color-primary-hover: #2563eb` - Hover state (blue-700)
- `--color-primary-dark: #1d4ed8` - Dark variant (blue-800)

### Accent Colors
- `--color-accent: #3b82f6` - Accent color for highlights
- `--color-success: #10b981` - Success states (green-500)
- `--color-warning: #f59e0b` - Warning states (amber-500)
- `--color-danger: #ef4444` - Error/danger states (red-500)
- `--color-info: #06b6d4` - Info states (cyan-500)

### Surface & Background
- `--color-surface: #ffffff` - Card/surface background (light mode)
- `--color-surface-raised: #f9fafb` - Elevated surfaces (light mode)
- `--color-surface-overlay: #ffffff` - Modal overlays (light mode)
- `--color-background: #f3f4f6` - Page background (light mode)

### Dark Mode Overrides
- `--color-surface: #1f2937` - Surface background (dark mode)
- `--color-surface-raised: #111827` - Elevated surfaces (dark mode)
- `--color-surface-overlay: #374151` - Modal overlays (dark mode)
- `--color-background: #111827` - Page background (dark mode)

### Text Colors
- `--color-text-primary: #111827` - Primary text (light mode) / `#f9fafb` (dark mode)
- `--color-text-secondary: #6b7280` - Secondary text (light mode) / `#d1d5db` (dark mode)
- `--color-text-tertiary: #9ca3af` - Tertiary/muted text
- `--color-text-inverse: #ffffff` - Inverse text color

### Border Colors
- `--color-border: #e5e7eb` - Default borders (light mode) / `#374151` (dark mode)
- `--color-border-focus: #3b82f6` - Focus state borders

## Spacing Scale

- `--spacing-xs: 0.25rem` (4px)
- `--spacing-sm: 0.5rem` (8px)
- `--spacing-md: 1rem` (16px)
- `--spacing-lg: 1.5rem` (24px)
- `--spacing-xl: 2rem` (32px)
- `--spacing-2xl: 3rem` (48px)

## Border Radius

- `--radius-sm: 0.25rem` (4px) - Small elements
- `--radius-md: 0.375rem` (6px) - Default
- `--radius-lg: 0.5rem` (8px) - Cards, modals
- `--radius-xl: 0.75rem` (12px) - Large elements

## Shadows

- `--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05)` - Subtle elevation
- `--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1)` - Cards
- `--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1)` - Modals, dropdowns

## Transitions

- `--transition-fast: 150ms ease-in-out` - Quick interactions
- `--transition-normal: 250ms ease-in-out` - Default
- `--transition-slow: 350ms ease-in-out` - Complex animations

## Z-Index Scale

- `--z-dropdown: 1000` - Dropdown menus
- `--z-modal: 2000` - Modal overlays
- `--z-toast: 3000` - Toast notifications
- `--z-tooltip: 4000` - Tooltips

## Usage Guidelines

### In CSS
```css
.my-component {
  background-color: var(--color-surface);
  color: var(--color-text-primary);
  border-radius: var(--radius-md);
  transition: var(--transition-normal);
}
```

### In Tailwind
Tokens are mapped in `tailwind.config.js`:
```javascript
colors: {
  accent: 'var(--color-accent)',
  danger: 'var(--color-danger)',
  surface: 'var(--color-surface)',
}
```

### Dark Mode
Dark mode is controlled via a class on the `<html>` element:
```html
<html class="dark">
```

Theme persistence is handled automatically by Alpine.js store in `/apps/ui/static/js/alpine-init.js`.

## Best Practices

1. **Always use design tokens** - Never use arbitrary colors or spacing values
2. **Maintain consistency** - Reuse existing tokens before creating new ones
3. **Document changes** - Update this file when adding new tokens
4. **Test both themes** - Verify changes work in both light and dark mode
5. **Accessibility** - Ensure sufficient color contrast (WCAG 2.1 AA minimum)
