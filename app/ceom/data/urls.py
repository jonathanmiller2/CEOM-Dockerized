#TODO: Is this conf import needed?
from django.conf.urls import *
from django.urls import re_path

import ceom.data.views

#TODO: is any of this needed?
urlpatterns = [
    #(r'^$', 'index'),
    re_path(r'^wms$', ceom.data.views.wms),
    re_path(r'^modis$', ceom.data.views.wms),
    re_path(r'^photos$', ceom.data.views.photos),
    #(r'^ecohealth$', 'ecohealth_wms'),
    re_path(r'^modis/(?P<product>\w{3,7})$', ceom.data.views.modis_wms),
]