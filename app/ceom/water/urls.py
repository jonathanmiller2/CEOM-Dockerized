#TODO: Are these imports necessary?
from django.conf.urls import *
from django.views.generic import TemplateView

from django.urls import re_path

urlpatterns = [
    
    re_path(r'^$', TemplateView.as_view(template_name="water/map.html")),
    re_path(r'overview/', TemplateView.as_view(template_name="water/overview.html")),
    re_path(r'CONUS-Water/', TemplateView.as_view(template_name="water/CONUS-Water.html")),
    re_path(r'GLOBAL-Water/', TemplateView.as_view(template_name="water/GLOBAL-Water.html")),
    re_path(r'33-year-wbfm/', TemplateView.as_view(template_name="water/33-year-wbfm.html")),
]

