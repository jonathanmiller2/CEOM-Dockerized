#TODO: Are these imports necessary?
from django.urls import path, re_path
from django.conf.urls import url, include
from filebrowser.sites import site
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.flatpages import views


from django.contrib.staticfiles.urls import staticfiles_urlpatterns #For dajaxice
urlpatterns = [
    re_path('^grappelli/', include('grappelli.urls')),
    re_path('^admin/', admin.site.urls),
    re_path('^admin/filebrowser/', site.urls),
    
    re_path(r'^tinymce/', include('tinymce.urls')),
    re_path(r'^captcha/', include('captcha.urls')),

    re_path(r'^accounts/', include('eomf.accounts.urls')),
    re_path(r'^modis/visualization/',include('eomf.visualization.urls')),
    re_path(r'^visualization/',include('eomf.visualization.urls')),
    re_path(r'^modis/data/',include('eomf.inventory.urls')),
    re_path(r'^inventory/',include('eomf.inventory.urls')),
    re_path(r'^data/',include('eomf.inventory.urls')),
    re_path(r'^geohealth/', include('eomf.geohealth.urls')),
    re_path(r'^photos/', include('eomf.photos.urls')),
    re_path(r'^birds/', include('eomf.birds.urls')),
    re_path(r'^h5n1/', include('eomf.h5n1.urls')),
 ##   # url(r'^service/', include('eomf.data.urls')),
    re_path(r'^gisday/', include('eomf.gisday.urls')),
    re_path(r'^contact/', TemplateView.as_view(template_name="contact.html")),
    re_path(r'^projects/', include('eomf.projects.urls')),
    re_path(r'^aboutus/',include('eomf.aboutus.urls')),
    re_path(r'^workshops/',include('eomf.workshops.urls')),
    re_path(r'^stats/', include('eomf.stats.urls')),
    re_path(r'^towers/', include('eomf.towers.urls')),
    re_path(r'^feedback/', include('eomf.feedback.urls')),
    re_path(r'^share/', include('eomf.eomfshare.urls')),
    re_path(r'^maps/', include('eomf.maps.urls')),
    re_path(r'^water/', include('eomf.water.urls')),
    # (r'^aoitest/', include('eomf.aoitest.urls')),
 ##   # (r'^poi/', include('eomf.poi.urls')),
 ##  # (r'^api/', include(entry_resource.urls)),

    re_path(r'^i18n/', include('django.conf.urls.i18n')),
 ##  # Json api
 #  url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
 #  url(r'^dajaxice/', include('dajaxice.urls')),
]

#Development only pages
if settings.DEBUG:
    #urlpatterns.append(url(r'^people/',include('eomf.people.urls')))
    #Append dev only urls here
    pass

from django.conf import settings

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls')),
    ]
#Catch all
urlpatterns += [
    path('<path:url>', views.flatpage),
]
