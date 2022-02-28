from django.views.generic import TemplateView
from django.urls import re_path
import ceom.tropomi.views

urlpatterns = [
    re_path(r'^$',  ceom.tropomi.views.index),
    
    re_path(r'^timeseries/single/$', ceom.tropomi.views.single),
    re_path(r'^timeseries/single/del=(?P<task_id>.+)/$', ceom.tropomi.views.single_del),
    re_path(r'^timeseries/single/t=(?P<task_id>.+)/$', ceom.tropomi.views.single_status),
    re_path(r'^timeseries/single/start/', ceom.tropomi.views.single_start),
    re_path(r'^timeseries/single/progress/t=(?P<task_id>.+)/$', ceom.tropomi.views.single_get_progress),
    re_path(r'^timeseries/single/history/$', ceom.tropomi.views.single_history),
    
    re_path(r'^timeseries/multiple/$', ceom.tropomi.views.multiple),
    re_path(r'^timeseries/multiple/del=(?P<task_id>.+)/$', ceom.tropomi.views.multiple_del),
    re_path(r'^timeseries/multiple/t=(?P<task_id>.+)$', ceom.tropomi.views.multiple_status),
    re_path(r'^timeseries/multiple/start/$', ceom.tropomi.views.multiple_start),
    re_path(r'^timeseries/multiple/progress/t=(?P<task_id>.+)/$', ceom.tropomi.views.multiple_get_progress),
    re_path(r'^timeseries/multiple/history/$', ceom.tropomi.views.multiple_history),
]
