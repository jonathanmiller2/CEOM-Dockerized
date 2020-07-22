from django.conf.urls import patterns, url, include
from django.contrib import admin
admin.autodiscover()

from views import handle_ajax

urlpatterns = patterns('eomf.feedback.views',
        (r'^ajax(?P<url>.*)$', handle_ajax),
        (r'^tracking/$', 'feedback_details'),
        (r'^comment/(?P<id>[0-9]+)','comment_page'),
    )

# vim: et sw=4 sts=4
