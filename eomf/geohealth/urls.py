from django.conf.urls import *

#TODO: These likely need to be instances of url(), if these pages aren't accessible, this is what needs to be changed
#'eomf.geohealth.views.####'
urlpatterns = [
    (r'^$', 'index'),
    (r'^kml/evi\.kml$','evi_kml'),
    (r'^kml/indices_(?P<name>.*)\.kml$','indices_kml'),
    (r'^kml/(?P<name>.*)\.kml$','kml'),
    (r'^kml/(?P<name>.*)\.kmz$','kml'),
    (r'.*', 'down'),
]
