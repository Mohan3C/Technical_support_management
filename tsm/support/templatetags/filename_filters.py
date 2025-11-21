import os
from django import template

register = template.Library()

@register.filter
def basename(value):
    return os.path.basename(value)  

"""os.path.basename(value) <-- Return the base filename without directories."""
