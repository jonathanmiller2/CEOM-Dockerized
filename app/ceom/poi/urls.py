#TODO: Are these imports necessary?
from django.conf.urls import *

from django.urls import re_path
import ceom.poi.views

urlpatterns = [
    re_path(r'^$', ceom.poi.views.home),
    re_path(r'^manage/$', ceom.poi.views.manage),
    re_path(r'^what_is_in_pixel/$', ceom.poi.views.wpixel),
    re_path(r'^add_research_pixels/$', ceom.poi.views.add_research_pixels),
    re_path(r'^create_research/$', ceom.poi.views.create_research),
    re_path(r'^edit_research/(?P<research_id>[0-9]+)/$', ceom.poi.views.edit_research),
    re_path(r'^get_research_pois/(?P<research_id>[0-9]+)/$', ceom.poi.views.get_research_pois)
]