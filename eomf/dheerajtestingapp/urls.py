from django.conf.urls import *
from django.views.generic import RedirectView

urlpatterns = patterns('eomf.dheerajtestingapp.views',
    (r'^test/$', 'dheerajViewFunction'),
)
