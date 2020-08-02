import os
from django import template
from django.conf import settings
from django.utils.safestring import SafeString
from eomf.pages.models import ContentPage

register = template.Library()

@register.filter 
def similar_pages(page):
    return ContentPage.objects.filter(url__startswith="/gisday/")

    slug = page.url[1:].split('/',2)[0]
    slug = '/'+slug+'/'
    pages = page.__class__.objects.filter(url__startswith=slug)

    return pages
