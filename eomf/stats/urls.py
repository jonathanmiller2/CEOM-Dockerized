from django.conf.urls import *
from django.views.generic import TemplateView
urlpatterns = patterns('eomf.stats.views',
	(r'^$', 'stats_main'),
	(r'^limit/(?P<year1>[0-9]{4})/(?P<year2>[0-9]{4})/$', 'stats_limit'),
	(r'^cumm/$', 'stats_cumm'),
	(r'^mont/(?P<year1>[0-9]{4})/(?P<year2>[0-9]{4})/$', 'stats_limit_mon'),
	(r'^mont/(?P<mon1>[0-9]{2})/(?P<day1>[0-9]{2})/(?P<year1>[0-9]{4})/(?P<mon2>[0-9]{2})/(?P<day2>[0-9]{2})/(?P<year2>[0-9]{4})/$', 'stats_limit_mon1'),
	(r'^phot/(?P<mon1>[0-9]{2})/(?P<day1>[0-9]{2})/(?P<year1>[0-9]{4})/(?P<mon2>[0-9]{2})/(?P<day2>[0-9]{2})/(?P<year2>[0-9]{4})/$', 'stats_limit_phot1'),
	(r'^phot/(?P<year1>[0-9]{4})/(?P<year2>[0-9]{4})/$', 'stats_limit_phot'),
	(r'^phot/cumm/$', 'stats_photo_cumm'),
	(r'^test_form/$', 'form_test'),
	(r'^search_form/$', 'search_frm'),
	#(r'^limit/$', 'stats_limit'),
)
