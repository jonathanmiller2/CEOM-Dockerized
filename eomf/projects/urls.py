from django.conf.urls import *
from eomf.projects.models import Project

from eomf.projects import views

urlpatterns = patterns('eomf.projects.views',
    (r'^$', 'index'),
)