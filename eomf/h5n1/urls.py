from django.conf.urls import *

urlpatterns = patterns('eomf.h5n1.views',
    (r'^$', 'index'),
    (r'^all.kml$', 'kml'),
)
