#TODO: Are these imports necessary?
from django.conf.urls import *
from django.views.generic import TemplateView

from django.urls import re_path
import eomf.gisday.views


urlpatterns = [
    re_path(r'^$', eomf.gisday.views.overview),
    re_path(r'^overview', eomf.gisday.views.overview),

    re_path(r'^2012/$', eomf.gisday.views.year2012),
    re_path(r'^2012/gallery', eomf.gisday.views.gallery_2012),

    re_path(r'^(?P<year>[0-9]{4})/summary','summary),
	re_path(r'^(?P<year>[0-9]{4})/agenda', eomf.gisday.views.agenda),
	re_path(r'^(?P<year>[0-9]{4})/logistics', eomf.gisday.views.logistics),
	re_path(r'^(?P<year>[0-9]{4})/announcements/(?P<position>[0-9]+)', eomf.gisday.views.announcements),
	re_path(r'^(?P<year>[0-9]{4})/announcements', eomf.gisday.views.announcements),
	re_path(r'^(?P<year>[0-9]{4})/aboutus', eomf.gisday.views.about_us),
	re_path(r'^(?P<year>[0-9]{4})/booth/update_(?P<id>[0-9]+)/email_(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', eomf.gisday.views.boothupdate),
	re_path(r'^(?P<year>[0-9]{4})/poster-contest/update_(?P<id>[0-9]+)/email_(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', eomf.gisday.views.posterupdate),
	re_path(r'^(?P<year>[0-9]{4})/guests', eomf.gisday.views.visitor_registration),
	re_path(r'^(?P<year>[0-9]{4})/sponsors', eomf.gisday.views.sponsors),
	re_path(r'^(?P<year>[0-9]{4})/photo-contest', eomf.gisday.views.photo_contest),
	re_path(r'^(?P<year>[0-9]{4})/poster-contest', eomf.gisday.views.poster_contest),
	re_path(r'^(?P<year>[0-9]{4})/photo-gallery', eomf.gisday.views.gallery),
	re_path(r'^(?P<year>[0-9]{4})/image-gallery', eomf.gisday.views.images),
    re_path(r'^(?P<year>[0-9]{4})/survey/', eomf.gisday.views.survey),
    re_path(r'^(?P<year>[0-9]{4})/survey', eomf.gisday.views.survey),
    re_path(r'^(?P<year>[0-9]{4})/demographic_survey', eomf.gisday.views.demographic_survey),

	# TODO: Is this needed?
	#(r'^(?P<year>[0-9]{4})/demograpichs_survey','demographic_survey),
    re_path(r'^(?P<year>[0-9]{4})/$', eomf.gisday.views.announcements),
    re_path(r'^(?P<year>[0-9]{4})/booth/$', eomf.gisday.views.booth),
    re_path(r'^(?P<year>[0-9]{4})/volunteer/$', eomf.gisday.views.volunteer),
]
# [\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}