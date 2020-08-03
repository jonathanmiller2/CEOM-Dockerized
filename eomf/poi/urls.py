#TODO: Are these imports necessary?
from django.conf.urls import *
from django.views.generic.simple import redirect_to

from django.urls import re_path
import eomf.poi.views

urlpatterns = [
    re_path(r'^$', eomf.poi.views.home),
    re_path(r'^manage/$', eomf.poi.views.manage),
    re_path(r'^what_is_in_pixel/$', eomf.poi.views.wpixel),
    # (r'^add$', 'addPixelValidation'),
    re_path(r'^add_research_pixels/$', eomf.poi.views.add_research_pixels),
    re_path(r'^create_research/$', eomf.poi.views.create_research),
    re_path(r'^edit_research/(?P<research_id>[0-9]+)/$', eomf.poi.views.edit_research),
    re_path(r'^get_research_pois/(?P<research_id>[0-9]+)/$', eomf.poi.views.get_research_pois)
]