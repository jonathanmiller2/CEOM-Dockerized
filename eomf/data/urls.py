from django.conf.urls import *

urlpatterns = patterns('data.views',
    #(r'^$', 'index'),
    (r'^wms$', 'wms'),
    (r'^modis$', 'wms'),
    (r'^photos$', 'photos'),
    #(r'^ecohealth$', 'ecohealth_wms'),
    (r'^modis/(?P<product>\w{3,7})$','modis_wms'),
)