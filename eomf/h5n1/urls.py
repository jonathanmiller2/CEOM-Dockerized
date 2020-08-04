#TODO: Is this import necessary?
from django.conf.urls import *

from django.urls import re_path
import eomf.h5n1.views

urlpatterns = [
    re_path(r'^$', eomf.h5n1.views.index),
    re_path(r'^all.kml$', eomf.h5n1.views.kml),
]
