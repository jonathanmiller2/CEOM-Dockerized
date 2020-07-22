from django.conf.urls import *
from django.views.generic.simple import redirect_to

urlpatterns = patterns('poi.views',
    (r'^$', 'home'),
    (r'^manage/$', 'manage'),
    (r'^what_is_in_pixel/$', 'wpixel'),
    # (r'^add$', 'addPixelValidation'),
    (r'^add_research_pixels/$', 'add_research_pixels'),
    (r'^create_research/$', 'create_research'),
    (r'^edit_research/(?P<research_id>[0-9]+)/$', 'edit_research'),
    (r'^get_research_pois/(?P<research_id>[0-9]+)/$','get_research_pois')
) 