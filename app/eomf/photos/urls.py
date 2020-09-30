#TODO: Are these imports necessary?
from django.conf.urls import *
from django.views.generic import RedirectView

from django.urls import re_path
import eomf.photos.views

urlpatterns = [
    re_path(r'^$', eomf.photos.views.home),
    re_path(r'^browse/$', eomf.photos.views.browse),
    re_path(r'^map/$', eomf.photos.views.map),
    re_path(r'^FieldPhoto/$', eomf.photos.views.FieldPhoto),
    #Personalized
    re_path(r'^cocorahs(?P<date>\w*)/$', eomf.photos.views.cocorahs),

    re_path(r'^user/$', eomf.photos.views.user_photos),
    re_path(r'^workset/$', eomf.photos.views.workset_photos),

    re_path(r'^download/$', eomf.photos.views.download),
    re_path(r'^batchedit/$', eomf.photos.views.batchedit),

    re_path(r'^upload/$', eomf.photos.views.upload, name='upload'),
    re_path(r'^preload/$', eomf.photos.views.preload),
    re_path(r'^upload/preload/$', eomf.photos.views.preload),
    re_path(r'^upload/preload/delete/(?P<name>.+)$', eomf.photos.views.preload_delete),
    
    #TODO: Are the extra mobile logins necessary? Currently using only #3 AFAIK
    re_path(r'^mobile/upload/$', eomf.photos.views.mobile_upload), #mobile upload view
    re_path(r'^mobile/upload2/$', eomf.photos.views.mobile_upload2), #mobile upload view
    re_path(r'^mobile/upload3/$', eomf.photos.views.mobile_upload3), #mobile upload view

    re_path(r'^view/(?P<id>\d+)/$', eomf.photos.views.view, name="photo-view"),
    re_path(r'^edit/(?P<id>\d+)/$', eomf.photos.views.edit, name="photo-edit"),
    re_path(r'^delete/(?P<id>\d+)/$', eomf.photos.views.delete, name="photo-del"),
    re_path(r'^exif/(?P<id>\d+)/$', eomf.photos.views.exif),

    #Data feeds
    re_path(r'^data.kml$', eomf.photos.views.kml),
    re_path(r'^clusters.kml$', eomf.photos.views.clusters),
    re_path(r'^clusters.php$', eomf.photos.views.clusters),
    re_path(r'^gmapclusters.kml$', eomf.photos.views.gmapclusters),
    re_path(r'^gmapclusters.php$', eomf.photos.views.gmapclusters),
    re_path(r'^photos.json$', eomf.photos.views.photos_json),
    re_path(r'^photos.html$', eomf.photos.views.photos_html),
    re_path(r'^photos2.html$', eomf.photos.views.photos_html2),
    #(r'^photos_near_coord/lat=(?P<lat>-?\d+(\.\d+)?)_lon=(?P<lon>-?\d+(\.\d+)?)_rad=(?P<radius>\d+(\.\d+)?)/$','photos_coord'),

    #Legacy redirects
    #TODO: DELETE ALL PHP FILES?
    #re_path(r'^map.php$', RedirectView.as_view(url='/photos/map/')),
    #re_path(r'^testmap.php$', RedirectView.as_view(url='/photos/testmap/')),
    #re_path(r'^query.php$',  RedirectView.as_view(url='/photos/browse/')),
    #re_path(r'^upload.php$',  RedirectView.as_view(url='/photos/upload/')),
]
