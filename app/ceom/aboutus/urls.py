from django.conf.urls import *
from django.urls import re_path
from django.views.generic import TemplateView
import ceom.aboutus.views

urlpatterns = [
    re_path(r'news/(?P<post_id>\d+)/$', ceom.aboutus.views.news),
    re_path(r'news/(?P<post_year>\d{4})/$', ceom.aboutus.views.news),
    re_path(r'news/$', ceom.aboutus.views.news),
    re_path(r'people', ceom.aboutus.views.people),
    re_path(r'research/projects/', TemplateView.as_view(template_name="aboutus/research/projects.html")),
    re_path(r'research/themes/', TemplateView.as_view(template_name="aboutus/research/themes.html")),
    re_path(r'research/$', TemplateView.as_view(template_name="aboutus/research/overview.html")),
    re_path(r'education/courses', TemplateView.as_view(template_name="aboutus/education/courses.html")),
    re_path(r'education/student_awards', TemplateView.as_view(template_name="aboutus/education/student_awards.html")),
    re_path(r'education/$', TemplateView.as_view(template_name="aboutus/education/overview.html")),
    re_path(r'facilities/clab/', TemplateView.as_view(template_name="aboutus/facilities/clab.html")),
    re_path(r'facilities/rslab/', TemplateView.as_view(template_name="aboutus/facilities/rslab.html")),
    re_path(r'facilities/isos/', TemplateView.as_view(template_name="aboutus/facilities/isos.html")),
    re_path(r'facilities/$', TemplateView.as_view(template_name="aboutus/facilities/overview.html")),
    re_path(r'calendar', TemplateView.as_view(template_name="aboutus/calendar.html")),
    re_path(r'publications/', ceom.aboutus.views.publications),
    re_path(r'^group_photos/(?P<selYear>\d{4})', ceom.aboutus.views.group_photos),
    re_path(r'^group_photos', ceom.aboutus.views.group_photos),
    re_path(r'$', ceom.aboutus.views.news),
    re_path(r'^stats_user/',ceom.aboutus.views.user_stats),
    re_path(r'^stats_photo/',ceom.aboutus.views.photo_stats),
]
