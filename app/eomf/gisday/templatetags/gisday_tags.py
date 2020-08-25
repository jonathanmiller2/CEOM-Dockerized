import os
from django import template
from django.conf import settings
from django.utils.safestring import SafeString
from django.contrib.flatpages.models import FlatPage

register = template.Library()

@register.filter 
def similar_pages(page):
    return FlatPage.objects.filter(url__startswith="/gisday/")

    slug = page.url[1:].split('/',2)[0]
    slug = '/'+slug+'/'
    pages = page.__class__.objects.filter(url__startswith=slug)

    return pages
