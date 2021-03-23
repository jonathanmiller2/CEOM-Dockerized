#TODO: Are these imports necessary?
from django.conf.urls import *
from django.views.generic import TemplateView

from django.urls import re_path
import ceom.outreach.workshops.views

urlpatterns = [
    #re_path(r'^$', ceom.outreach.workshops.views.overview),
    re_path(r'^overview', ceom.outreach.workshops.views.overview),
    re_path(r'^current/(?P<year>\d+)', ceom.outreach.workshops.views.workshop_list_by_year_current),
    re_path(r'^current/', ceom.outreach.workshops.views.workshop_current),
    re_path(r'^past/(?P<year>\d+)', ceom.outreach.workshops.views.workshop_list_by_year_past),
    re_path(r'^past/', ceom.outreach.workshops.views.workshop_past),
    re_path(r'^content/(?P<workshop_id>\d+)', ceom.outreach.workshops.views.workshop),
    re_path(r'^register/(?P<workshop_id>\d+)', ceom.outreach.workshops.views.workshop_registration),
    re_path(r'^presentations/(?P<workshop_id>\d+)', ceom.outreach.workshops.views.presentations),
    re_path(r'^photos/(?P<workshop_id>\d+)', ceom.outreach.workshops.views.photos),
]
