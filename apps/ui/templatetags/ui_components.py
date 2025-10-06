"""
UI component template tags for MetaTasks.
Following specification Section 31.8 Template Tag Helpers
"""

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_button(
    label,
    variant="primary",
    size="md",
    icon=None,
    href=None,
    type="button",
    **attrs
):
    """
    Render a button component with specified variant and size.
    
    Variants: primary, secondary, subtle, danger, ghost
    Sizes: sm, md, lg
    """
    css_classes = ["btn", f"btn-{variant}"]
    
    if size != "md":
        css_classes.append(f"btn-{size}")
    
    # Add any additional CSS classes
    if "class" in attrs:
        css_classes.append(attrs.pop("class"))
    
    # Build attributes string
    attr_str = " ".join([f'{k}="{v}"' for k, v in attrs.items()])
    
    # Icon HTML if provided
    icon_html = ""
    if icon:
        icon_html = f'<svg class="w-4 h-4 mr-2" aria-hidden="true"><use href="#{icon}"></use></svg>'
    
    # Build the HTML
    if href:
        return format_html(
            '<a href="{}" class="{}" {}>{}{}</a>',
            href,
            " ".join(css_classes),
            mark_safe(attr_str),
            mark_safe(icon_html),
            label,
        )
    else:
        return format_html(
            '<button type="{}" class="{}" {}>{}{}</button>',
            type,
            " ".join(css_classes),
            mark_safe(attr_str),
            mark_safe(icon_html),
            label,
        )


@register.simple_tag
def badge(text, status="neutral"):
    """
    Render a status badge.
    
    Status: success, warning, danger, info, neutral
    """
    css_class = f"badge badge-{status}"
    return format_html('<span class="{}">{}</span>', css_class, text)


@register.simple_tag
def usage_meter(current, limit, label=None):
    """
    Render a usage meter/progress bar.
    
    Returns a progress bar with percentage and optional label.
    """
    if limit == 0 or limit is None:
        percentage = 0
        status = "success"
    else:
        percentage = min((current / limit) * 100, 100)
        
        # Determine status color based on usage
        if percentage >= 90:
            status = "danger"
        elif percentage >= 75:
            status = "warning"
        else:
            status = "success"
    
    label_html = ""
    if label:
        label_html = f'<div class="text-sm text-gray-600 dark:text-gray-400 mb-1">{label}</div>'
    
    return format_html(
        '{}'
        '<div class="progress-bar">'
        '  <div class="progress-fill progress-fill-{}" style="width: {}%"></div>'
        '</div>'
        '<div class="text-xs text-gray-500 dark:text-gray-400 mt-1">'
        '  {}/{} ({}%)'
        '</div>',
        mark_safe(label_html),
        status,
        percentage,
        current,
        limit if limit else "∞",
        int(percentage),
    )


@register.simple_tag
def alert(message, alert_type="info", dismissible=False):
    """
    Render an alert component.
    
    Types: success, warning, danger, info
    """
    dismiss_btn = ""
    if dismissible:
        dismiss_btn = (
            '<button type="button" class="ml-auto text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200" '
            'onclick="this.parentElement.remove()" aria-label="Close">'
            '<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">'
            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>'
            '</svg></button>'
        )
    
    return format_html(
        '<div class="alert alert-{} flex items-center" role="alert">'
        '  <div class="flex-1">{}</div>'
        '  {}'
        '</div>',
        alert_type,
        message,
        mark_safe(dismiss_btn),
    )


@register.simple_tag
def form_field(field, label=None, help_text=None, required=False):
    """
    Render a form field with label, error handling, and help text.
    """
    field_id = field.auto_id if hasattr(field, 'auto_id') else f"id_{field.name}"
    field_label = label or (field.label if hasattr(field, 'label') else field.name)
    field_help = help_text or (field.help_text if hasattr(field, 'help_text') else '')
    field_errors = field.errors if hasattr(field, 'errors') else []
    
    required_html = '<span class="text-red-500">*</span>' if required else ''
    
    help_html = ""
    if field_help:
        help_html = f'<p class="form-help" id="{field_id}-help">{field_help}</p>'
    
    error_html = ""
    if field_errors:
        error_html = f'<p class="form-error" id="{field_id}-error" role="alert">{field_errors[0]}</p>'
    
    aria_attrs = []
    if field_help:
        aria_attrs.append(f'aria-describedby="{field_id}-help"')
    if field_errors:
        aria_attrs.append(f'aria-describedby="{field_id}-error"')
        aria_attrs.append('aria-invalid="true"')
    
    return format_html(
        '<div class="form-group">'
        '  <label for="{}" class="form-label">{} {}</label>'
        '  <input type="text" id="{}" name="{}" class="form-input" {} />'
        '  {}'
        '  {}'
        '</div>',
        field_id,
        field_label,
        mark_safe(required_html),
        field_id,
        field.name if hasattr(field, 'name') else 'field',
        mark_safe(' '.join(aria_attrs)),
        mark_safe(help_html),
        mark_safe(error_html),
    )


@register.simple_tag
def icon(name, css_class="w-5 h-5"):
    """
    Render an SVG icon using Heroicons or custom icon set.
    """
    # Common Heroicons
    icons = {
        'check': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>',
        'x': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>',
        'plus': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>',
        'pencil': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>',
        'trash': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>',
        'search': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>',
        'menu': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>',
        'bell': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>',
        'cog': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>',
        'user': '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>',
    }
    
    icon_path = icons.get(name, icons['check'])
    
    return format_html(
        '<svg class="{}" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">{}</svg>',
        css_class,
        mark_safe(icon_path),
    )


@register.filter
def status_badge(status):
    """
    Filter to convert status string to badge HTML.
    Usage: {{ workitem.status|status_badge }}
    """
    status_map = {
        'pending': ('neutral', 'Pending'),
        'in_progress': ('info', 'In Progress'),
        'completed': ('success', 'Completed'),
        'failed': ('danger', 'Failed'),
        'cancelled': ('warning', 'Cancelled'),
    }
    
    badge_type, badge_text = status_map.get(status.lower(), ('neutral', status))
    return format_html('<span class="badge badge-{}">{}</span>', badge_type, badge_text)
