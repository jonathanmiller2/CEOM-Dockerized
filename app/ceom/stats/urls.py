#TODO: Are these imports necessary?
from django.conf.urls import *
from django.views.generic import TemplateView

from django.urls import re_path
import ceom.stats.views

urlpatterns = [
	re_path(r'^$', ceom.stats.views.stats_main),
	re_path(r'^limit/(?P<year1>[0-9]{4})/(?P<year2>[0-9]{4})/$', ceom.stats.views.stats_limit),
	re_path(r'^cumm/$', ceom.stats.views.stats_cumm),
	re_path(r'^mont/(?P<year1>[0-9]{4})/(?P<year2>[0-9]{4})/$', ceom.stats.views.stats_limit_mon),
	re_path(r'^mont/(?P<mon1>[0-9]{2})/(?P<day1>[0-9]{2})/(?P<year1>[0-9]{4})/(?P<mon2>[0-9]{2})/(?P<day2>[0-9]{2})/(?P<year2>[0-9]{4})/$', ceom.stats.views.stats_limit_mon1),
	re_path(r'^phot/(?P<mon1>[0-9]{2})/(?P<day1>[0-9]{2})/(?P<year1>[0-9]{4})/(?P<mon2>[0-9]{2})/(?P<day2>[0-9]{2})/(?P<year2>[0-9]{4})/$', ceom.stats.views.stats_limit_phot1),
	re_path(r'^phot/(?P<year1>[0-9]{4})/(?P<year2>[0-9]{4})/$', ceom.stats.views.stats_limit_phot),
	re_path(r'^phot/cumm/$', ceom.stats.views.stats_photo_cumm),
	re_path(r'^test_form/$', ceom.stats.views.form_test),
	re_path(r'^search_form/$', ceom.stats.views.search_frm),
	#(r'^limit/$', 'stats_limit'),
]
