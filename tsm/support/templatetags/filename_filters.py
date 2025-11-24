import os
from django import template

register = template.Library()

@register.filter
def basename(value):
    return os.path.basename(value)  

"""os.path.basename(value) <-- Return the base filename without directories."""

# this didn`t work `

# @register.simple_tag(takes_context=True)
# def nav_active(context, url):
#     request = context["request"]
#     return "aria-current=\"page\"" if request.path == url else ""
