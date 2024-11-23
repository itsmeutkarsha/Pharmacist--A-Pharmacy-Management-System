# core/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    print(f"Getting attribute '{attr_name}' from object '{obj}'")  # Debugging line
    return getattr(obj, attr_name, None)
