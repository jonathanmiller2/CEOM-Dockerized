#TODO: Are these imports necessary?
from django.conf.urls import *
from django.views.generic import TemplateView

from django.urls import re_path
import ceom.inventory.views

urlpatterns = [
    re_path(r'^(?P<dataset_id>m\w{5,6})/(?P<year>\d{4})/$', ceom.inventory.views.tilemap),
    re_path(r'^tile-h(?P<x>\d+)v(?P<y>\d+)$', ceom.inventory.views.tile),
    re_path(r'^tile-details-h(?P<x>\d+)v(?P<y>\d+)$', ceom.inventory.views.tile_details),
	re_path(r'^remote_sensing_datasets/', ceom.inventory.views.remote_sensing_datasets),
	re_path(r'^global_gis_data/', TemplateView.as_view(template_name="/inventory/under_construction.html")),
	re_path(r'^regional_gis_data/', TemplateView.as_view(template_name="/inventory/under_construction.html")),
	re_path(r'^country_gis_data/', TemplateView.as_view(template_name="/inventory/under_construction.html")),
	re_path(r'^subcountry_gis_data/', TemplateView.as_view(template_name="/inventory/under_construction.html")),
	re_path(r'^$', ceom.inventory.views.remote_sensing_datasets),
]
