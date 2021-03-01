#TODO: Are these imports necessary?
from django.conf.urls import *
from ceom.projects.models import Project

from django.urls import re_path
import ceom.projects.views



urlpatterns = [
    re_path(r'^$', ceom.projects.views.index),
]