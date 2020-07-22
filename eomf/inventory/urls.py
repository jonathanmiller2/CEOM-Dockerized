from django.conf.urls import *
from django.views.generic import TemplateView
urlpatterns = patterns('eomf.inventory.views',
    (r'^(?P<dataset_id>m\w{5,6})/(?P<year>\d{4})/$', 'tilemap'),
    (r'^tile-h(?P<x>\d+)v(?P<y>\d+)$', 'tile'),
    (r'^tile-details-h(?P<x>\d+)v(?P<y>\d+)$', 'tile_details'),
	(r'^remote_sensing_datasets/', 'remote_sensing_datasets'),
	(r'^global_gis_data/', TemplateView.as_view(template_name="/inventory/under_construction.html")),
	(r'^regional_gis_data/', TemplateView.as_view(template_name="/inventory/under_construction.html")),
	(r'^country_gis_data/', TemplateView.as_view(template_name="/inventory/under_construction.html")),
	(r'^subcountry_gis_data/', TemplateView.as_view(template_name="/inventory/under_construction.html")),
	(r'^$', 'remote_sensing_datasets'),
)
