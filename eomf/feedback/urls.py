from django.conf.urls import url, include
from django.contrib import admin
admin.autodiscover()

from eomf.feedback.views import handle_ajax

#TODO: These likely need to be instances of url(), if these pages aren't accessible, this is what needs to be changed
#eomf.feedback.views
urlpatterns = [
        (r'^ajax(?P<url>.*)$', handle_ajax),
        (r'^tracking/$', 'feedback_details'),
        (r'^comment/(?P<id>[0-9]+)','comment_page'),
]

# vim: et sw=4 sts=4
