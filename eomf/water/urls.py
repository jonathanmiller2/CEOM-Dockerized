from django.conf.urls import *
from django.views.generic import TemplateView

#TODO: These likely need to be instances of url(), if these pages aren't accessible, this is what needs to be changed
#eomf.water.views
urlpatterns = [
    
    (r'^$', TemplateView.as_view(template_name="water/map.html")),
    (r'overview/', TemplateView.as_view(template_name="water/overview.html")),
    (r'CONUS-Water/', TemplateView.as_view(template_name="water/CONUS-Water.html")),
    (r'GLOBAL-Water/', TemplateView.as_view(template_name="water/GLOBAL-Water.html")),
    (r'33-year-wbfm/', TemplateView.as_view(template_name="water/33-year-wbfm.html")),
]

