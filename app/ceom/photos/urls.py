#TODO: Are these imports necessary?
from django.conf.urls import *
from django.views.generic import RedirectView

from django.urls import re_path
import ceom.photos.views

urlpatterns = [
    re_path(r'^$', ceom.photos.views.home),
    re_path(r'^browse/$', ceom.photos.views.browse),
    re_path(r'^map/$', ceom.photos.views.map),
    re_path(r'^FieldPhoto/?$', ceom.photos.views.FieldPhoto),
   
    re_path(r'^user/?$', ceom.photos.views.user_photos),

    re_path(r'^download/$', ceom.photos.views.download),
    re_path(r'^batchedit/$', ceom.photos.views.batchedit),

    re_path(r'^upload/$', ceom.photos.views.upload, name='upload'),
    re_path(r'^preload/$', ceom.photos.views.preload),
    re_path(r'^upload/preload/$', ceom.photos.views.preload),
    re_path(r'^upload/preload/delete/(?P<name>.+)$', ceom.photos.views.preload_delete),
    
    re_path(r'^mobile/upload/?$', ceom.photos.views.mobile_upload), #mobile upload view

    re_path(r'^view/(?P<id>\d+)/?$', ceom.photos.views.view, name="photo-view"),
    re_path(r'^edit/(?P<id>\d+)/?$', ceom.photos.views.edit, name="photo-edit"),
    re_path(r'^delete/(?P<id>\d+)/?$', ceom.photos.views.delete, name="photo-del"),
    re_path(r'^exif/(?P<id>\d+)/?$', ceom.photos.views.exif),

    #Data feeds
    re_path(r'^data.kml$', ceom.photos.views.kml),
    re_path(r'^clusters.kml$', ceom.photos.views.clusters),
    re_path(r'^clusters.php$', ceom.photos.views.clusters),
    re_path(r'^gmapclusters.kml$', ceom.photos.views.gmapclusters),
    re_path(r'^gmapclusters.php$', ceom.photos.views.gmapclusters),
    re_path(r'^photos.json$', ceom.photos.views.photos_json),
]
