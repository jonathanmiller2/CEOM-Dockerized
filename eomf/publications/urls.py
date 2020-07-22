from django.conf.urls import *
from eomf.publications.models import Publication

info_dict = {
	'queryset': Publication.objects.all(),
}

urlpatterns = patterns('eomf.publications.views',
    (r'^$', 'index'),
    (r'^(?P<object_id>\d+)/$', 'detail')
)
