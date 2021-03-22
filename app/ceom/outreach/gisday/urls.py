#TODO: Are these imports necessary?
from django.conf.urls import *
from django.views.generic import TemplateView

from django.urls import re_path
import ceom.outreach.gisday.views


urlpatterns = [
    re_path(r'^$', ceom.outreach.gisday.views.overview),
    re_path(r'^gisday/overview', ceom.outreach.gisday.views.overview),

    re_path(r'^2012/$', ceom.outreach.gisday.views.year2012),
    re_path(r'^2012/gallery', ceom.outreach.gisday.views.gallery_2012),

    re_path(r'^(?P<year>[0-9]{4})/summary', ceom.outreach.gisday.views.summary),
	re_path(r'^(?P<year>[0-9]{4})/agenda', ceom.outreach.gisday.views.agenda),
	re_path(r'^(?P<year>[0-9]{4})/logistics', ceom.outreach.gisday.views.logistics),
	re_path(r'^(?P<year>[0-9]{4})/announcements/(?P<position>[0-9]+)', ceom.outreach.gisday.views.announcements),
	re_path(r'^(?P<year>[0-9]{4})/announcements', ceom.outreach.gisday.views.announcements),
	re_path(r'^(?P<year>[0-9]{4})/aboutus', ceom.outreach.gisday.views.about_us),
	re_path(r'^(?P<year>[0-9]{4})/booth/update_(?P<id>[0-9]+)/email_(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', ceom.outreach.gisday.views.boothupdate),
	re_path(r'^(?P<year>[0-9]{4})/poster-contest/update_(?P<id>[0-9]+)/email_(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', ceom.outreach.gisday.views.posterupdate),
	re_path(r'^(?P<year>[0-9]{4})/guests', ceom.outreach.gisday.views.visitor_registration),
	re_path(r'^(?P<year>[0-9]{4})/sponsors', ceom.outreach.gisday.views.sponsors),
	re_path(r'^(?P<year>[0-9]{4})/photo-contest', ceom.outreach.gisday.views.photo_contest),
	re_path(r'^(?P<year>[0-9]{4})/poster-contest', ceom.outreach.gisday.views.poster_contest),
	re_path(r'^(?P<year>[0-9]{4})/photo-gallery', ceom.outreach.gisday.views.gallery),
	re_path(r'^(?P<year>[0-9]{4})/image-gallery', ceom.outreach.gisday.views.images),
    re_path(r'^(?P<year>[0-9]{4})/survey/', ceom.outreach.gisday.views.survey),
    re_path(r'^(?P<year>[0-9]{4})/survey', ceom.outreach.gisday.views.survey),
    re_path(r'^(?P<year>[0-9]{4})/demographic_survey', ceom.outreach.gisday.views.demographic_survey),

	# TODO: Is this needed?
	#(r'^(?P<year>[0-9]{4})/demograpichs_survey','demographic_survey),
    re_path(r'^(?P<year>[0-9]{4})/$', ceom.outreach.gisday.views.announcements),
    re_path(r'^(?P<year>[0-9]{4})/booth/$', ceom.outreach.gisday.views.booth),
    re_path(r'^(?P<year>[0-9]{4})/volunteer/$', ceom.outreach.gisday.views.volunteer),
]
# [\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}