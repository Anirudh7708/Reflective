from django import template

register = template.Library()


@register.filter
def get_range(value):
    """Convert a number into a range of numbers starting from 0"""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)


@register.filter
def subtract(value, arg):
    """Subtract the arg from the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0
