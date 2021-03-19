#TODO: Are these imports necessary?
from django.conf.urls import *
from django.views.generic import TemplateView

from django.urls import re_path
import ceom.outreach.views


urlpatterns = [
    re_path(r'^$', ceom.outreach.views.gisday_overview),

    re_path(r'^overview', ceom.outreach.views.gisday_overview),
    re_path(r'^workshop/overview', ceom.outreach.views.workshop_overview),

    #re_path(r'^2012/$', ceom.outreach.views.year2012),
    #re_path(r'^2012/gallery', ceom.outreach.views.gallery_2012),

    re_path(r'^(?P<year>[0-9]{4})/summary', ceom.outreach.views.summary),
	re_path(r'^(?P<year>[0-9]{4})/agenda', ceom.outreach.views.agenda),
	re_path(r'^(?P<year>[0-9]{4})/logistics', ceom.outreach.views.logistics),
	re_path(r'^(?P<year>[0-9]{4})/announcements/(?P<position>[0-9]+)', ceom.outreach.views.announcements),
	re_path(r'^(?P<year>[0-9]{4})/announcements', ceom.outreach.views.announcements),
	re_path(r'^(?P<year>[0-9]{4})/aboutus', ceom.outreach.views.about_us),
	re_path(r'^(?P<year>[0-9]{4})/booth/update_(?P<id>[0-9]+)/email_(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', ceom.outreach.views.boothupdate),
	re_path(r'^(?P<year>[0-9]{4})/poster-contest/update_(?P<id>[0-9]+)/email_(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', ceom.outreach.views.posterupdate),
	re_path(r'^(?P<year>[0-9]{4})/guests', ceom.outreach.views.visitor_registration),
	re_path(r'^(?P<year>[0-9]{4})/sponsors', ceom.outreach.views.sponsors),
	re_path(r'^(?P<year>[0-9]{4})/photo-contest', ceom.outreach.views.photo_contest),
	re_path(r'^(?P<year>[0-9]{4})/poster-contest', ceom.outreach.views.poster_contest),
	re_path(r'^(?P<year>[0-9]{4})/photo-gallery', ceom.outreach.views.gallery),
	re_path(r'^(?P<year>[0-9]{4})/image-gallery', ceom.outreach.views.images),
    re_path(r'^(?P<year>[0-9]{4})/survey/', ceom.outreach.views.survey),
    re_path(r'^(?P<year>[0-9]{4})/survey', ceom.outreach.views.survey),
    re_path(r'^(?P<year>[0-9]{4})/demographic_survey', ceom.outreach.views.demographic_survey),

	# TODO: Is this needed?
	#(r'^(?P<year>[0-9]{4})/demograpichs_survey','demographic_survey),
    re_path(r'^(?P<year>[0-9]{4})/$', ceom.outreach.views.announcements),
    re_path(r'^(?P<year>[0-9]{4})/booth/$', ceom.outreach.views.booth),
    re_path(r'^(?P<year>[0-9]{4})/volunteer/$', ceom.outreach.views.volunteer),

    
    re_path(r'^current/(?P<year>\d+)', ceom.outreach.views.workshop_list_by_year_current),
    re_path(r'^current/', ceom.outreach.views.workshop_current),
    re_path(r'^workshop/past/(?P<year>\d+)', ceom.outreach.views.workshop_list_by_year_past),
    re_path(r'^workshop/past/', ceom.outreach.views.workshop_past),
    re_path(r'^content/(?P<workshop_id>\d+)', ceom.outreach.views.workshop),
    re_path(r'^register/(?P<workshop_id>\d+)', ceom.outreach.views.workshop_registration),
    re_path(r'^presentations/(?P<workshop_id>\d+)', ceom.outreach.views.presentations),
    re_path(r'^photos/(?P<workshop_id>\d+)', ceom.outreach.views.photos),
]
