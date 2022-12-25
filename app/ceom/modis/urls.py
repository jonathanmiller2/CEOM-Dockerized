from django.urls import re_path, path
import ceom.modis.views

modis_re =  r'(?P<dataset>[mM]\w{6})(?:-(?P<product>\w{3,4}))?_(?P<years>(\d{4})?(,\d{4})*)_(?P<lat>-?\d+(\.\d+)?)_(?P<lon>-?\d+(\.\d+)?)'

urlpatterns = [
    re_path(r'^$',  ceom.modis.views.index),
    re_path(r'^vimap/$', ceom.modis.views.vimap),
    
    re_path(r'^inventory/(?P<dataset_id>[mM]\w{5,6})/(?P<year>\d{4})/$', ceom.modis.views.tilemap),
    re_path(r'^(?P<dataset_id>[mM]\w{5,6})/tile-h(?P<x>\d+)v(?P<y>\d+)/$', ceom.modis.views.tile),
	re_path(r'^remote_sensing_datasets/', ceom.modis.views.remote_sensing_datasets),
	
    re_path(r'^timeseries/single/$', ceom.modis.views.single),
    re_path(r'^timeseries/single/del=(?P<task_id>.+)/$', ceom.modis.views.single_del),
    re_path(r'^timeseries/single/t=(?P<task_id>.+)/$', ceom.modis.views.single_status),
    re_path(r'^timeseries/single/progress/t=(?P<task_id>.+)/$', ceom.modis.views.single_get_progress),
    re_path(r'^timeseries/single/history/$', ceom.modis.views.single_history),
    
    re_path(r'^timeseries/multiple/$', ceom.modis.views.multiple),
    re_path(r'^timeseries/multiple/del=(?P<task_id>.+)/$', ceom.modis.views.multiple_del),
    re_path(r'^timeseries/multiple/t=(?P<task_id>.+)/$', ceom.modis.views.multiple_status),
    re_path(r'^timeseries/multiple/progress/t=(?P<task_id>.+)/$', ceom.modis.views.multiple_get_progress),
    re_path(r'^timeseries/multiple/history/$', ceom.modis.views.multiple_history),
    
    re_path(r'^composite/(?P<year>\d{4})/(?P<julian_day>\d*)/$', ceom.modis.views.composite),
    re_path(r'^composite/', ceom.modis.views.composite),
]
