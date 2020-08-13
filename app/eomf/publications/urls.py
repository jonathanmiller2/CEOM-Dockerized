#TODO: Are these imports necessary?
from django.conf.urls import *
from eomf.publications.models import Publication

from django.urls import re_path
import eomf.publications.views

info_dict = {
	'queryset': Publication.objects.all(),
}

urlpatterns = [
    re_path(r'^$', eomf.publications.views.index),
    re_path(r'^(?P<object_id>\d+)/$', eomf.publications.views.detail)
]
