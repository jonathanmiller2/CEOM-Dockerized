#TODO: Are these imports necessary?
from django.conf.urls import url
from django.views.generic import TemplateView

from django.urls import re_path
import ceom.modis.visualization.views

modis_re =  r'(?P<dataset>[mM]\w{6})(?:-(?P<product>\w{3,4}))?_(?P<years>(\d{4})?(,\d{4})*)_(?P<lat>-?\d+(\.\d+)?)_(?P<lon>-?\d+(\.\d+)?)'


urlpatterns = [
    re_path(r'^$',  ceom.modis.visualization.views.index),
    #(r'^test/$',  ceom.modis.visualization.views.test),
    re_path(r'^kml/evi\.kml$', ceom.modis.visualization.views.evi_kml),
    re_path(r'^kml/indices_(?P<name>.*)\.kml$', ceom.modis.visualization.views.indices_kml),
    re_path(r'^kml/(?P<name>.*)\.kml$', ceom.modis.visualization.views.kml),
    re_path(r'^kml/(?P<name>.*)\.kmz$', ceom.modis.visualization.views.kml),
    re_path(r'^olmap/$', ceom.modis.visualization.views.olmap),
    re_path(r'^gemap/$', ceom.modis.visualization.views.gemap),
    re_path(r'^gmap/$', ceom.modis.visualization.views.gmap),
    re_path(r'^gmap/(?P<lat>-?\d+(\.\d+)?)_(?P<lon>-?\d+(\.\d+)?)', ceom.modis.visualization.views.gmap1),
    re_path(r'^manual/$', ceom.modis.visualization.views.manual),
    re_path(r'^multiple/$', ceom.modis.visualization.views.multiple),
    re_path(r'^multiple/del=(?P<del_id>[0-9]+)/$', ceom.modis.visualization.views.multiple_del),
    re_path(r'^multiple_add/$', ceom.modis.visualization.views.multiple_add),
    
    re_path(r'^timeseries/single/$', ceom.modis.visualization.views.timeseries_single_history),
    re_path(r'^timeseries/single/add/$', ceom.modis.visualization.views.gmap),
    re_path(r'^timeseries/single/del=(?P<del_id>[0-9]+)/$', ceom.modis.visualization.views.single_del),
    re_path(r'^timeseries/single/t=(?P<task_id>.+)/$', ceom.modis.visualization.views.timeseries_single_progress),
    re_path(r'^timeseries/single/start/'+modis_re+'/', ceom.modis.visualization.views.launch_single_site_timeseries),
    re_path(r'^timeseries/single/progress/t=(?P<task_id>.+)/$', ceom.modis.visualization.views.get_task_progress),

    re_path(r'^geocatter/$', ceom.modis.visualization.views.geocatter),
    re_path(r'^get_multiple_task_progress/$', ceom.modis.visualization.views.get_multiple_task_progress),
    
    # Now visualization works differently
    # (r'^ascii_'+modis_re+r'.txt$', ceom.modis.visualization.views.ascii'),
    # (r'^csv_'+modis_re+r'.csv$', ceom.modis.visualization.views.csv_content'),
    # (r'^csv_products_'+modis_re+r'.csv$', ceom.modis.visualization.views.csv_products'),
    # (r'^csv_products_graphs_'+modis_re+r'.csv$', ceom.modis.visualization.views.csv_products_graphs'),
    # (r'^graph-'+modis_re+r'$', ceom.modis.visualization.views.graphlist'),
    # (r'^graph_'+modis_re+r'_(?P<band>.+).png$', ceom.modis.visualization.views.graph'),
    # (r'^graphjs-'+modis_re+r'$', ceom.modis.visualization.views.graphlist_js'),
    # (r'^graphjs2-'+modis_re,'graphlist_js_prod'),
    
    re_path(r'^composite/(?P<year>\d{4})/(?P<julian_day>\d*)/$', ceom.modis.visualization.views.composite),
    re_path(r'^composite', ceom.modis.visualization.views.composite),
    
# r'mod=\d+_h=\d+_v=\d+_r=\d+_c=\d+_lc1=\d+;\d(?:_lc2=\d+;\d+)?(?:_lc3=\d+;\d+)?$'
    #(r'.*', ceom.visualization.views.down'),
]
