from django.conf.urls import *
from django.views.generic import TemplateView
urlpatterns = patterns('eomf.towers.views',
	(r'^$', 'tower_main'),
)
