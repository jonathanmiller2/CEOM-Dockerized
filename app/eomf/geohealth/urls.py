#TODO: Is this import needed?
from django.conf.urls import *

from django.urls import re_path
import eomf.geohealth.views

urlpatterns = [
    re_path(r'^$', eomf.geohealth.views.index),
    re_path(r'^kml/evi\.kml$', eomf.geohealth.views.evi_kml),
    re_path(r'^kml/indices_(?P<name>.*)\.kml$', eomf.geohealth.views.indices_kml),
    re_path(r'^kml/(?P<name>.*)\.kml$', eomf.geohealth.views.kml),
    re_path(r'^kml/(?P<name>.*)\.kmz$', eomf.geohealth.views.kml),
    re_path(r'.*', eomf.geohealth.views.down),
]
