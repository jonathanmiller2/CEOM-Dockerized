#TODO: Are these imports necessary?
from django.conf.urls import url
from django.views.generic import TemplateView

from django.urls import re_path
import eomf.visualization.views

modis_re =  r'(?P<dataset>[mM]\w{6})(?:-(?P<product>\w{3,4}))?_(?P<years>(\d{4})?(,\d{4})*)_(?P<lat>-?\d+(\.\d+)?)_(?P<lon>-?\d+(\.\d+)?)'


urlpatterns = [
    re_path(r'^$',  eomf.visualization.views.index),
    #(r'^test/$',  eomf.visualization.views.test),
    re_path(r'^kml/evi\.kml$', eomf.visualization.views.evi_kml),
    re_path(r'^kml/indices_(?P<name>.*)\.kml$', eomf.visualization.views.indices_kml),
    re_path(r'^kml/(?P<name>.*)\.kml$', eomf.visualization.views.kml),
    re_path(r'^kml/(?P<name>.*)\.kmz$', eomf.visualization.views.kml),
    re_path(r'^olmap/$', eomf.visualization.views.olmap),
    re_path(r'^gemap/$', eomf.visualization.views.gemap),
    re_path(r'^gmap/$', eomf.visualization.views.gmap),
    re_path(r'^gmap/(?P<lat>-?\d+(\.\d+)?)_(?P<lon>-?\d+(\.\d+)?)', eomf.visualization.views.gmap1),
    re_path(r'^manual/$', eomf.visualization.views.manual),
    re_path(r'^multiple/$', eomf.visualization.views.multiple),
    re_path(r'^multiple/del=(?P<del_id>[0-9]+)/$', eomf.visualization.views.multiple_del),
    re_path(r'^multiple_add/$', eomf.visualization.views.multiple_add),
    
    re_path(r'^timeseries/single/$', eomf.visualization.views.timeseries_single_history),
    re_path(r'^timeseries/single/add/$', eomf.visualization.views.gmap),
    re_path(r'^timeseries/single/del=(?P<del_id>[0-9]+)/$', eomf.visualization.views.single_del),
    re_path(r'^timeseries/single/t=(?P<task_id>.+)/$', eomf.visualization.views.timeseries_single_progress),
    re_path(r'^timeseries/single/graphs/t=(?P<task_id>.+)/$', eomf.visualization.views.timeseries_single_chart),
    re_path(r'^timeseries/single/start/'+modis_re+'/', eomf.visualization.views.launch_single_site_timeseries),
    re_path(r'^timeseries/single/start/c6/'+modis_re+'/', eomf.visualization.views.launch_single_site_timeseries_c6),

    
    # Now visualization works differently
    # (r'^ascii_'+modis_re+r'.txt$', eomf.visualization.views.ascii'),
    # (r'^csv_'+modis_re+r'.csv$', eomf.visualization.views.csv_content'),
    # (r'^csv_products_'+modis_re+r'.csv$', eomf.visualization.views.csv_products'),
    # (r'^csv_products_graphs_'+modis_re+r'.csv$', eomf.visualization.views.csv_products_graphs'),
    # (r'^graph-'+modis_re+r'$', eomf.visualization.views.graphlist'),
    # (r'^graph_'+modis_re+r'_(?P<band>.+).png$', eomf.visualization.views.graph'),
    # (r'^graphjs-'+modis_re+r'$', eomf.visualization.views.graphlist_js'),
    # (r'^graphjs2-'+modis_re,'graphlist_js_prod'),
    
    re_path(r'^composite/(?P<year>\d{4})/(?P<julian_day>\d*)/$', eomf.visualization.views.composite),
    re_path(r'^composite', eomf.visualization.views.composite),


# r'mod=\d+_h=\d+_v=\d+_r=\d+_c=\d+_lc1=\d+;\d(?:_lc2=\d+;\d+)?(?:_lc3=\d+;\d+)?$'
    #(r'.*', eomf.visualization.views.down'),
]
