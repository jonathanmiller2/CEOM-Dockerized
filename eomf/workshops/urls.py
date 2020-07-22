from django.conf.urls import *
from django.views.generic import TemplateView

urlpatterns = patterns('eomf.workshops.views',
    (r'^$','overview' ),
    (r'^current/(?P<year>\d+)','workshop_list_by_year_current' ),
    (r'^current/','workshop_current' ),
    (r'^past/(?P<year>\d+)','workshop_list_by_year_past' ),
    (r'^past/','workshop_past'),
    (r'^content/(?P<workshop_id>\d+)','workshop'),
    (r'^register/(?P<workshop_id>\d+)','workshop_registration'),
    (r'^presentations/(?P<workshop_id>\d+)','presentations'),
    (r'^photos/(?P<workshop_id>\d+)','photos'),
	)
