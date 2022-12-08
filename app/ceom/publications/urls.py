#TODO: Are these imports necessary?
from django.conf.urls import *
from ceom.aboutus.models import Publication

from django.urls import re_path
import ceom.publications.views

info_dict = {
	'queryset': Publication.objects.all(),
}

urlpatterns = [
    re_path(r'^$', ceom.publications.views.index),
    re_path(r'^(?P<object_id>\d+)/$', ceom.publications.views.detail)
]
