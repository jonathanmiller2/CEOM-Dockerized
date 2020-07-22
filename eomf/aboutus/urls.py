from django.conf.urls import *
from django.views.generic import TemplateView


urlpatterns = patterns('eomf.aboutus.views',
    (r'news/(?P<post_id>\d+)/$', 'news' ),
    (r'news/(?P<post_year>\d{4})/$', 'news'),
    (r'news/$', 'news'),
    (r'people', 'people'),
    (r'research/projects/', TemplateView.as_view(template_name="aboutus/research/projects.html")),
    (r'research/themes/', TemplateView.as_view(template_name="aboutus/research/themes.html")),
    (r'research/$', TemplateView.as_view(template_name="aboutus/research/overview.html")),
    (r'education/courses', TemplateView.as_view(template_name="aboutus/education/courses.html")),
    (r'education/student_awards', TemplateView.as_view(template_name="aboutus/education/student_awrdas.html")),
    (r'education/$', TemplateView.as_view(template_name="aboutus/education/overview.html")),
    (r'facilities/clab/', TemplateView.as_view(template_name="aboutus/facilities/clab.html")),
    (r'facilities/vlab/', TemplateView.as_view(template_name="aboutus/facilities/vlab.html")),   
    (r'facilities/rslab/', TemplateView.as_view(template_name="aboutus/facilities/rslab.html")),
    (r'facilities/isos/', TemplateView.as_view(template_name="aboutus/facilities/isos.html")),
    (r'facilities/$', TemplateView.as_view(template_name="aboutus/facilities/overview.html")),
	(r'calendar', TemplateView.as_view(template_name="aboutus/calendar.html")),
	(r'^publications/', include('eomf.publications.urls')),
	(r'^group_photos/(?P<selYear>\d{4})', 'group_photos'),
	(r'^group_photos', 'group_photos'),
    (r'bhargavbolla/', 'bhrgvbolla'),
    (r'$', 'news'),
    (r'dd/$', TemplateView.as_view(template_name="aboutus/dheeraj_demo/trail.html")),
    

)
