from django.conf.urls import *

urlpatterns = patterns('eomf.geohealth.views',
    (r'^$', 'index'),
    (r'^kml/evi\.kml$','evi_kml'),
    (r'^kml/indices_(?P<name>.*)\.kml$','indices_kml'),
    (r'^kml/(?P<name>.*)\.kml$','kml'),
    (r'^kml/(?P<name>.*)\.kmz$','kml'),
    (r'.*', 'down'),
)
