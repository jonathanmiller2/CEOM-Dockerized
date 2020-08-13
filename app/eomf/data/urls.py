#TODO: Is this conf import needed?
from django.conf.urls import *
from django.urls import re_path

import eomf.data.views

#TODO: is any of this needed?
urlpatterns = [
    #(r'^$', 'index'),
    re_path(r'^wms$', eomf.data.views.wms),
    re_path(r'^modis$', eomf.data.views.wms),
    re_path(r'^photos$', eomf.data.views.photos),
    #(r'^ecohealth$', 'ecohealth_wms'),
    re_path(r'^modis/(?P<product>\w{3,7})$', eomf.data.views.modis_wms),
]