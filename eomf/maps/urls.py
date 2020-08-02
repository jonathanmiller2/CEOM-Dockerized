from django.conf.urls import *
from django.views.generic import TemplateView

#TODO: These likely need to be instances of url(), if these pages aren't accessible, this is what needs to be changed
#eomf.maps.views
urlpatterns = [
	(r'^roi/$', 'ROI'),#Regions of interest.
	(r'^poi/$', 'POI'),#Points of interest.
	(r'^view_rois/$', 'VIEW_ROI'),#All ROI's
	(r'^download_rois/$', 'test_kml'),#Test download
	(r'^filter_rois/$', 'filter_kml'),#Test download
	(r'^view_pois/$', 'VIEW_POI'),#All POI's
	(r'^map_gallery/$', 'VIEW_MAPS'),#Viewing uploaded maps
	(r'^detail_map_gallery/(?P<id>[0-9]+)', 'DETAIL_MAP'),#Viewing uploaded maps
	(r'^add_map_gallery/$', 'ADD_MAPS'),#Adding new maps
]
