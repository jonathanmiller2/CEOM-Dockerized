from django.conf.urls import *
from django.views.generic import TemplateView


urlpatterns = patterns('eomf.gisday.views',
    (r'^$', 'overview'),
    (r'^overview', 'overview'),
    
    (r'^2012/$', 'year2012'),
    (r'^2012/gallery', 'gallery_2012'),
    
    (r'^(?P<year>[0-9]{4})/summary','summary'),
	(r'^(?P<year>[0-9]{4})/agenda', 'agenda'),
	(r'^(?P<year>[0-9]{4})/logistics', 'logistics'),
	(r'^(?P<year>[0-9]{4})/announcements/(?P<position>[0-9]+)', 'announcements'),
	(r'^(?P<year>[0-9]{4})/announcements', 'announcements'),
	(r'^(?P<year>[0-9]{4})/aboutus', 'about_us'),
	(r'^(?P<year>[0-9]{4})/booth/update_(?P<id>[0-9]+)/email_(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', 'boothupdate'),
	(r'^(?P<year>[0-9]{4})/poster-contest/update_(?P<id>[0-9]+)/email_(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', 'posterupdate'),
	(r'^(?P<year>[0-9]{4})/guests', 'visitor_registration'),
	(r'^(?P<year>[0-9]{4})/sponsors', 'sponsors'),
	(r'^(?P<year>[0-9]{4})/photo-contest', 'photo_contest'),
	(r'^(?P<year>[0-9]{4})/poster-contest', 'poster_contest'),
	(r'^(?P<year>[0-9]{4})/photo-gallery', 'gallery'),
	(r'^(?P<year>[0-9]{4})/image-gallery', 'images'),
    (r'^(?P<year>[0-9]{4})/survey/','survey'),
    (r'^(?P<year>[0-9]{4})/survey','survey'),
    (r'^(?P<year>[0-9]{4})/demographic_survey','demographic_survey'),
    (r'^(?P<year>[0-9]{4})/demograpichs_survey','demographic_survey'),
    (r'^(?P<year>[0-9]{4})/$','announcements'),
    (r'^(?P<year>[0-9]{4})/booth/$', 'booth'),
    (r'^(?P<year>[0-9]{4})/volunteer/$', 'volunteer'),

	

)
# [\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}