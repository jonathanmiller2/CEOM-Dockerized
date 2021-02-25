#TODO: Are these imports necessary?
from django.conf.urls import *
from django.views.generic import TemplateView

from django.urls import re_path
import ceom.towers.views

urlpatterns = [
	re_path(r'^$', ceom.towers.views.tower_main),
]
