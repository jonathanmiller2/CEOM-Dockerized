#TODO: Are these imports necessary?
from django.conf.urls import *
from django.views.generic import TemplateView

from django.urls import re_path
import eomf.maps.views

urlpatterns = [
	re_path(r'^roi/$', eomf.maps.views.ROI),#Regions of interest.
	re_path(r'^poi/$', eomf.maps.views.POI),#Points of interest.
	re_path(r'^view_rois/$', eomf.maps.views.VIEW_ROI),#All ROI's
	re_path(r'^download_rois/$', eomf.maps.views.test_kml),#Test download
	re_path(r'^filter_rois/$', eomf.maps.views.filter_kml),#Test download
	re_path(r'^view_pois/$', eomf.maps.views.VIEW_POI),#All POI's
	re_path(r'^map_gallery/$', eomf.maps.views.VIEW_MAPS),#Viewing uploaded maps
	re_path(r'^detail_map_gallery/(?P<id>[0-9]+)', eomf.maps.views.DETAIL_MAP),#Viewing uploaded maps
	re_path(r'^add_map_gallery/$', eomf.maps.views.ADD_MAPS),#Adding new maps
]
