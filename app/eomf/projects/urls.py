#TODO: Are these imports necessary?
from django.conf.urls import *
from eomf.projects.models import Project

from django.urls import re_path
import eomf.projects.views



urlpatterns = [
    re_path(r'^$', eomf.projects.views.index),
]