from django import template
from django.template import engines
from django.template.defaultfilters import stringfilter
from django.template import Context
register = template.Library()

@register.filter
@stringfilter
def render(value):
    return engines['django'].from_string(value).render()
