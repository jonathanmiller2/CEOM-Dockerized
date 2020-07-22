from django.conf.urls import *

urlpatterns = patterns('eomf.pages.views',
    (r'^(?P<url>.*)$', 'contentpage'),
)
