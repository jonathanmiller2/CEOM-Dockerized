from django.conf.urls import *
from django.views.generic import TemplateView

#TODO: These likely need to be instances of url(), if these pages aren't accessible, this is what needs to be changed
#eomf.towers.views
urlpatterns = [
	(r'^$', 'tower_main'),
]
