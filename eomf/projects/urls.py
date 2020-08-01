from django.conf.urls import *
from eomf.projects.models import Project

from eomf.projects import views

#TODO: These likely need to be instances of url(), if these pages aren't accessible, this is what needs to be changed
#eomf.projects.views
urlpatterns = [
    (r'^$', 'index'),
]