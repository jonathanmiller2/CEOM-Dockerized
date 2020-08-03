#TODO: Is this import necessary?
from django.conf.urls import *

from django.urls import re_path
import eomf.h5n1.views

urlpatterns = [
    (r'^$', eomf.h5n1.views.index),
    (r'^all.kml$', eomf.h5n1.views.kml),
]
