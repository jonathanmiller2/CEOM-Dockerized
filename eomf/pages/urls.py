from django.conf.urls import *

#TODO: These likely need to be instances of url(), if these pages aren't accessible, this is what needs to be changed
#eomf.pages.views
urlpatterns = [
    (r'^(?P<url>.*)$', 'contentpage'),
]
