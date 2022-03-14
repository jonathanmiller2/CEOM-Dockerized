from django.conf.urls import *
from django.views.generic import TemplateView

from django.urls import re_path, path
import ceom.modis.views

modis_re =  r'(?P<dataset>[mM]\w{6})(?:-(?P<product>\w{3,4}))?_(?P<years>(\d{4})?(,\d{4})*)_(?P<lat>-?\d+(\.\d+)?)_(?P<lon>-?\d+(\.\d+)?)'

urlpatterns = [
    re_path(r'^(?P<dataset_id>[mM]\w{5,6})/(?P<year>\d{4})/$', ceom.modis.views.tilemap),
    re_path(r'^tile-h(?P<x>\d+)v(?P<y>\d+)$', ceom.modis.views.tile),
    re_path(r'^tile-details-h(?P<x>\d+)v(?P<y>\d+)$', ceom.modis.views.tile_details),
	re_path(r'^remote_sensing_datasets/', ceom.modis.views.remote_sensing_datasets),
	re_path(r'^global_gis_data/', TemplateView.as_view(template_name="/under_construction.html")),
	re_path(r'^regional_gis_data/', TemplateView.as_view(template_name="/under_construction.html")),
	re_path(r'^country_gis_data/', TemplateView.as_view(template_name="/under_construction.html")),
	re_path(r'^subcountry_gis_data/', TemplateView.as_view(template_name="/under_construction.html")),
	#re_path(r'^$', ceom.modis.views.remote_sensing_datasets),
	re_path(r'^$',  ceom.modis.views.index),
    #(r'^test/$',  ceom.modis.views.test),
    re_path(r'^kml/evi\.kml$', ceom.modis.views.evi_kml),
    re_path(r'^kml/indices_(?P<name>.*)\.kml$', ceom.modis.views.indices_kml),
    re_path(r'^kml/(?P<name>.*)\.kml$', ceom.modis.views.kml),
    re_path(r'^kml/(?P<name>.*)\.kmz$', ceom.modis.views.kml),
    re_path(r'^olmap/$', ceom.modis.views.olmap),
    re_path(r'^gemap/$', ceom.modis.views.gemap),
    re_path(r'^gmap/$', ceom.modis.views.gmap),
    re_path(r'^gmap/(?P<lat>-?\d+(\.\d+)?)_(?P<lon>-?\d+(\.\d+)?)', ceom.modis.views.gmap1),
    re_path(r'^manual/$', ceom.modis.views.manual),
    re_path(r'^multiple/$', ceom.modis.views.multiple),
    re_path(r'^multiple/del=(?P<del_id>[0-9]+)/$', ceom.modis.views.multiple_del),
    re_path(r'^multiple_add/$', ceom.modis.views.multiple_add),
    
    re_path(r'^timeseries/single/$', ceom.modis.views.timeseries_single_history),
    re_path(r'^timeseries/single/add/$', ceom.modis.views.gmap),
    re_path(r'^timeseries/single/del=(?P<del_id>[0-9]+)/$', ceom.modis.views.single_del),
    re_path(r'^timeseries/single/t=(?P<task_id>.+)/$', ceom.modis.views.timeseries_single_progress),
    re_path(r'^timeseries/single/start/'+modis_re+'/', ceom.modis.views.launch_single_site_timeseries),
    re_path(r'^timeseries/single/progress/t=(?P<task_id>.+)/$', ceom.modis.views.get_task_progress),

    re_path(r'^geocatter/$', ceom.modis.views.geocatter),
    re_path(r'^get_multiple_task_progress/$', ceom.modis.views.get_multiple_task_progress),
    
    # Now visualization works differently
    # (r'^ascii_'+modis_re+r'.txt$', ceom.modis.visualization.views.ascii'),
    # (r'^csv_'+modis_re+r'.csv$', ceom.modis.visualization.views.csv_content'),
    # (r'^csv_products_'+modis_re+r'.csv$', ceom.modis.visualization.views.csv_products'),
    # (r'^csv_products_graphs_'+modis_re+r'.csv$', ceom.modis.visualization.views.csv_products_graphs'),
    # (r'^graph-'+modis_re+r'$', ceom.modis.visualization.views.graphlist'),
    # (r'^graph_'+modis_re+r'_(?P<band>.+).png$', ceom.modis.visualization.views.graph'),
    # (r'^graphjs-'+modis_re+r'$', ceom.modis.visualization.views.graphlist_js'),
    # (r'^graphjs2-'+modis_re,'graphlist_js_prod'),
    
    re_path(r'^composite/(?P<year>\d{4})/(?P<julian_day>\d*)/$', ceom.modis.views.composite),
    re_path(r'^composite', ceom.modis.views.composite),

    re_path(r'^tropomi/', ceom.modis.views.tropomi),
    re_path(r'^tropomi/(?P<lat>-?\d+(\.\d+)?)_(?P<lon>-?\d+(\.\d+)?)', ceom.modis.views.tropomi1),


	# r'mod=\d+_h=\d+_v=\d+_r=\d+_c=\d+_lc1=\d+;\d(?:_lc2=\d+;\d+)?(?:_lc3=\d+;\d+)?$'
    #(r'.*', ceom.visualization.views.down'),

]
