from django.conf.urls import *
from django.views.generic import RedirectView

import eomf.photos.views

#TODO: These likely need to be instances of url(), if these pages aren't accessible, this is what needs to be changes
#eomf.photos.views.###
urlpatterns = [
    (r'^$', 'home'),
    (r'^browse/$', 'browse'),
    (r'^map/$', 'map'),
    (r'^testmap/$', 'testmap'),
    (r'^FieldPhoto/$', 'FieldPhoto'),
    #Personalized
    (r'^cocorahs(?P<date>\w*)/$', 'cocorahs'),

    (r'^user/$', 'user_photos'),
    (r'^workset/$', 'workset_photos'),

    (r'^download/$', 'download'),
    (r'^batchedit/$', 'batchedit'),

    url(r'^upload/$', eomf.photos.views.upload, name='upload'),
    (r'^preload/$', 'preload'),
    (r'^upload/preload/$', 'preload'),
    (r'^upload/preload/delete/(?P<name>.+)$', 'preload_delete'),
    (r'^mobile/upload/$', 'mobile_upload'), #mobile upload view
    (r'^mobile/upload2/$', 'mobile_upload2'), #mobile upload view
    url(r'^mobile/upload3/$', eomf.photos.views.mobile_upload3), #mobile upload view

    url(r'^view/(?P<id>\d+)/$', eomf.photos.views.view, name="photo-view"),
    url(r'^edit/(?P<id>\d+)/$', eomf.photos.views.edit, name="photo-edit"),
    url(r'^delete/(?P<id>\d+)/$', eomf.photos.views.delete, name="photo-del"),
    (r'^exif/(?P<id>\d+)/$', 'exif'),

    #Data feeds
    (r'^data.kml$','kml'),
    (r'^clusters.kml$', 'clusters'),
    (r'^clusters.php$', 'clusters'),
    (r'^gmapclusters.kml$', 'gmapclusters'),
    (r'^gmapclusters.php$', 'gmapclusters'),
    (r'^photos.json$', 'photos_json'),
    (r'^photos.html$', 'photos_html'),
    (r'^photos2.html$', 'photos_html2'),
    #(r'^photos_near_coord/lat=(?P<lat>-?\d+(\.\d+)?)_lon=(?P<lon>-?\d+(\.\d+)?)_rad=(?P<radius>\d+(\.\d+)?)/$','photos_coord'),

    #Legacy redirects
    (r'^map.php$', RedirectView.as_view(url='/photos/map/')),
    (r'^testmap.php$', RedirectView.as_view(url='/photos/testmap/')),
    (r'^query.php$',  RedirectView.as_view(url='/photos/browse/')),
    (r'^upload.php$',  RedirectView.as_view(url='/photos/upload/')),
]
