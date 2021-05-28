from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def render(value):
    return get_template_from_string(value).render(Context())
