#TODO: Are these imports necessary?
from django.conf.urls import *
from django.views.generic import TemplateView

from django.urls import re_path
import eomf.outreach.views


urlpatterns = [
    re_path(r'^$', eomf.outreach.views.overview),

    re_path(r'^overview', eomf.outreach.views.overview),

    re_path(r'^2012/$', eomf.outreach.views.year2012),
    re_path(r'^2012/gallery', eomf.outreach.views.gallery_2012),

    re_path(r'^(?P<year>[0-9]{4})/summary', eomf.outreach.views.summary),
	re_path(r'^(?P<year>[0-9]{4})/agenda', eomf.outreach.views.agenda),
	re_path(r'^(?P<year>[0-9]{4})/logistics', eomf.outreach.views.logistics),
	re_path(r'^(?P<year>[0-9]{4})/announcements/(?P<position>[0-9]+)', eomf.outreach.views.announcements),
	re_path(r'^(?P<year>[0-9]{4})/announcements', eomf.outreach.views.announcements),
	re_path(r'^(?P<year>[0-9]{4})/aboutus', eomf.outreach.views.about_us),
	re_path(r'^(?P<year>[0-9]{4})/booth/update_(?P<id>[0-9]+)/email_(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', eomf.outreach.views.boothupdate),
	re_path(r'^(?P<year>[0-9]{4})/poster-contest/update_(?P<id>[0-9]+)/email_(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', eomf.outreach.views.posterupdate),
	re_path(r'^(?P<year>[0-9]{4})/guests', eomf.outreach.views.visitor_registration),
	re_path(r'^(?P<year>[0-9]{4})/sponsors', eomf.outreach.views.sponsors),
	re_path(r'^(?P<year>[0-9]{4})/photo-contest', eomf.outreach.views.photo_contest),
	re_path(r'^(?P<year>[0-9]{4})/poster-contest', eomf.outreach.views.poster_contest),
	re_path(r'^(?P<year>[0-9]{4})/photo-gallery', eomf.outreach.views.gallery),
	re_path(r'^(?P<year>[0-9]{4})/image-gallery', eomf.outreach.views.images),
    re_path(r'^(?P<year>[0-9]{4})/survey/', eomf.outreach.views.survey),
    re_path(r'^(?P<year>[0-9]{4})/survey', eomf.outreach.views.survey),
    re_path(r'^(?P<year>[0-9]{4})/demographic_survey', eomf.outreach.views.demographic_survey),

	# TODO: Is this needed?
	#(r'^(?P<year>[0-9]{4})/demograpichs_survey','demographic_survey),
    re_path(r'^(?P<year>[0-9]{4})/$', eomf.outreach.views.announcements),
    re_path(r'^(?P<year>[0-9]{4})/booth/$', eomf.outreach.views.booth),
    re_path(r'^(?P<year>[0-9]{4})/volunteer/$', eomf.outreach.views.volunteer),

    
    re_path(r'^current/(?P<year>\d+)', eomf.outreach.views.workshop_list_by_year_current),
    re_path(r'^current/', eomf.outreach.views.workshop_current),
    re_path(r'^past/(?P<year>\d+)', eomf.outreach.views.workshop_list_by_year_past),
    re_path(r'^past/', eomf.outreach.views.workshop_past),
    re_path(r'^content/(?P<workshop_id>\d+)', eomf.outreach.views.workshop),
    re_path(r'^register/(?P<workshop_id>\d+)', eomf.outreach.views.workshop_registration),
    re_path(r'^presentations/(?P<workshop_id>\d+)', eomf.outreach.views.presentations),
    re_path(r'^photos/(?P<workshop_id>\d+)', eomf.outreach.views.photos),
]
