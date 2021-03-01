#TODO: Is this import needed?
from django.conf.urls import *

from django.urls import re_path
import ceom.geohealth.views

urlpatterns = [
    re_path(r'^$', ceom.geohealth.views.index),
    re_path(r'^kml/evi\.kml$', ceom.geohealth.views.evi_kml),
    re_path(r'^kml/indices_(?P<name>.*)\.kml$', ceom.geohealth.views.indices_kml),
    re_path(r'^kml/(?P<name>.*)\.kml$', ceom.geohealth.views.kml),
    re_path(r'^kml/(?P<name>.*)\.kmz$', ceom.geohealth.views.kml),
    re_path(r'.*', ceom.geohealth.views.down),
]
