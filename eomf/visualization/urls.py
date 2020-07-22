from django.conf.urls import url, patterns
from django.views.generic import TemplateView

modis_re =  r'(?P<dataset>[mM]\w{6})(?:-(?P<product>\w{3,4}))?_(?P<years>(\d{4})?(,\d{4})*)_(?P<lat>-?\d+(\.\d+)?)_(?P<lon>-?\d+(\.\d+)?)'
urlpatterns = patterns('eomf.visualization.views',
    (r'^$', 'index'),
    #(r'^test/$', 'test'),
    (r'^kml/evi\.kml$','evi_kml'),
    (r'^kml/indices_(?P<name>.*)\.kml$','indices_kml'),
    (r'^kml/(?P<name>.*)\.kml$','kml'),
    (r'^kml/(?P<name>.*)\.kmz$','kml'),
    (r'^olmap/$', 'olmap'),
    (r'^gemap/$', 'gemap'),
    (r'^gmap/$', 'gmap'),
    (r'^gmap/(?P<lat>-?\d+(\.\d+)?)_(?P<lon>-?\d+(\.\d+)?)', 'gmap1'),
    (r'^manual/$', 'manual'),
    (r'^multiple/$', 'multiple'),
    (r'^multiple/del=(?P<del_id>[0-9]+)/$', 'multiple_del'),
    (r'^multiple_add/$', 'multiple_add'),
    
    (r'^timeseries/single/$', 'timeseries_single_history'),
    (r'^timeseries/single/add/$', 'gmap'),
    (r'^timeseries/single/del=(?P<del_id>[0-9]+)/$', 'single_del'),
    (r'^timeseries/single/t=(?P<task_id>.+)/$', 'timeseries_single_progress'),
    (r'^timeseries/single/graphs/t=(?P<task_id>.+)/$', 'timeseries_single_chart'),
    (r'^timeseries/single/start/'+modis_re+'/','launch_single_site_timeseries'),
    (r'^timeseries/single/start/c6/'+modis_re+'/','launch_single_site_timeseries_c6'),

    
    # Now visualization works differently
    # (r'^ascii_'+modis_re+r'.txt$', 'ascii'),
    # (r'^csv_'+modis_re+r'.csv$', 'csv_content'),
    # (r'^csv_products_'+modis_re+r'.csv$', 'csv_products'),
    # (r'^csv_products_graphs_'+modis_re+r'.csv$', 'csv_products_graphs'),
    # (r'^graph-'+modis_re+r'$', 'graphlist'),
    # (r'^graph_'+modis_re+r'_(?P<band>.+).png$', 'graph'),
    # (r'^graphjs-'+modis_re+r'$', 'graphlist_js'),
    # (r'^graphjs2-'+modis_re,'graphlist_js_prod'),
    
    (r'^composite/(?P<year>\d{4})/(?P<julian_day>\d*)/$', 'composite'),
    (r'^composite', 'composite'),


# r'mod=\d+_h=\d+_v=\d+_r=\d+_c=\d+_lc1=\d+;\d(?:_lc2=\d+;\d+)?(?:_lc3=\d+;\d+)?$'
    #(r'.*', 'down'),
)
