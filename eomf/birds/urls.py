from django.conf.urls import *

urlpatterns = patterns('eomf.birds.views',
    (r'^$', 'index'),
    (r'^all.kml$', 'kml'),
)
