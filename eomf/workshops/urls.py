#TODO: Are these imports necessary?
from django.conf.urls import *
from django.views.generic import TemplateView

from django.urls import re_path
import eomf.workshops.views

urlpatterns = [
    re_path(r'^$', eomf.workshops.views.overview),
    re_path(r'^current/(?P<year>\d+)', eomf.workshops.views.workshop_list_by_year_current),
    re_path(r'^current/', eomf.workshops.views.workshop_current),
    re_path(r'^past/(?P<year>\d+)', eomf.workshops.views.workshop_list_by_year_past),
    re_path(r'^past/', eomf.workshops.views.workshop_past),
    re_path(r'^content/(?P<workshop_id>\d+)', eomf.workshops.views.workshop),
    re_path(r'^register/(?P<workshop_id>\d+)', eomf.workshops.views.workshop_registration),
    re_path(r'^presentations/(?P<workshop_id>\d+)', eomf.workshops.views.presentations),
    re_path(r'^photos/(?P<workshop_id>\d+)', eomf.workshops.views.photos),
]
