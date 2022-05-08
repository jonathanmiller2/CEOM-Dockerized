from django.conf.urls import *
from django.views.generic import TemplateView

from django.urls import re_path, path
import ceom.modis.views

modis_re =  r'(?P<dataset>[mM]\w{6})(?:-(?P<product>\w{3,4}))?_(?P<years>(\d{4})?(,\d{4})*)_(?P<lat>-?\d+(\.\d+)?)_(?P<lon>-?\d+(\.\d+)?)'

urlpatterns = [
    re_path(r'^$',  ceom.modis.views.index),
    re_path(r'^vimap/$', ceom.modis.views.vimap),
    re_path(r'^geocatter/$', ceom.modis.views.geocatter),
    
    re_path(r'^(?P<dataset_id>[mM]\w{5,6})/(?P<year>\d{4})/$', ceom.modis.views.tilemap),
    re_path(r'^tile-h(?P<x>\d+)v(?P<y>\d+)$', ceom.modis.views.tile),
	re_path(r'^remote_sensing_datasets/', ceom.modis.views.remote_sensing_datasets),
	
    re_path(r'^kml/evi\.kml$', ceom.modis.views.evi_kml),
    re_path(r'^kml/indices_(?P<name>.*)\.kml$', ceom.modis.views.indices_kml),
    re_path(r'^kml/(?P<name>.*)\.kml$', ceom.modis.views.kml),
    re_path(r'^kml/(?P<name>.*)\.kmz$', ceom.modis.views.kml),

    re_path(r'^timeseries/single/$', ceom.modis.views.single),
    re_path(r'^timeseries/single/del=(?P<del_id>[0-9]+)/$', ceom.modis.views.single_del),
    re_path(r'^timeseries/single/t=(?P<task_id>.+)/$', ceom.modis.views.timeseries_single_progress),
    re_path(r'^timeseries/single/start/'+modis_re+'/', ceom.modis.views.launch_single_site_timeseries),
    re_path(r'^timeseries/single/progress/t=(?P<task_id>.+)/$', ceom.modis.views.get_task_progress),

    re_path(r'^timeseries/multiple/$', ceom.modis.views.multiple),
    re_path(r'^timeseries/multiple/del=(?P<del_id>[0-9]+)/$', ceom.modis.views.multiple_del),
    re_path(r'^timeseries/get_multiple_task_progress/$', ceom.modis.views.get_multiple_task_progress),
    
    re_path(r'^composite/(?P<year>\d{4})/(?P<julian_day>\d*)/$', ceom.modis.views.composite),
    re_path(r'^composite/', ceom.modis.views.composite),
]
