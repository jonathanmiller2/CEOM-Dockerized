from django.conf.urls import *
from eomf.publications.models import Publication

info_dict = {
	'queryset': Publication.objects.all(),
}

#TODO: These likely need to be instances of url(), if these pages aren't accessible, this is what needs to be changed
#eomf.publications.views
urlpatterns = [
    (r'^$', 'index'),
    (r'^(?P<object_id>\d+)/$', 'detail')
]
