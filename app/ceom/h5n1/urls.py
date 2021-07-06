from django.urls import re_path
import ceom.h5n1.views

urlpatterns = [
    re_path(r'^$', ceom.h5n1.views.index),
    re_path(r'^all.kml$', ceom.h5n1.views.kml),
]
