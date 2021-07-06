from django.urls import path, re_path
from django.conf.urls import url, include
from filebrowser.sites import site
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView


from django.contrib.staticfiles.urls import staticfiles_urlpatterns #For dajaxice
urlpatterns = [
    re_path('^grappelli/', include('grappelli.urls')),
    re_path('^admin/', admin.site.urls),
    re_path('^admin/filebrowser/', site.urls),
    
    re_path(r'^tinymce/', include('tinymce.urls')),
    re_path(r'^captcha/', include('captcha.urls')),

    re_path(r'^accounts/', include('ceom.accounts.urls')),
    re_path(r'^modis/visualization/',include('ceom.visualization.urls')),
    re_path(r'^visualization/',include('ceom.visualization.urls')),
    re_path(r'^modis/data/',include('ceom.inventory.urls')),
    re_path(r'^inventory/',include('ceom.inventory.urls')),
    re_path(r'^data/',include('ceom.inventory.urls')),
    re_path(r'^geohealth/', include('ceom.geohealth.urls')),
    re_path(r'^photos/', include('ceom.photos.urls')),
    re_path(r'^birds/', include('ceom.birds.urls')),
    re_path(r'^h5n1/', include('ceom.h5n1.urls')),
 ##   # url(r'^service/', include('ceom.data.urls')),
    re_path(r'^contact/', TemplateView.as_view(template_name="contact.html")),
    re_path(r'^aboutus/',include('ceom.aboutus.urls')),
    re_path(r'^outreach/workshops/', include('ceom.outreach.workshops.urls')),
    re_path(r'^outreach/gisday/', include('ceom.outreach.gisday.urls')),
    re_path(r'^stats/', include('ceom.stats.urls')),
    re_path(r'^towers/', include('ceom.towers.urls')),
    re_path(r'^maps/', include('ceom.maps.urls')),
    re_path(r'^water/', include('ceom.water.urls')),
    # (r'^aoitest/', include('ceom.aoitest.urls')),
 ##   # (r'^poi/', include('ceom.poi.urls')),
 ##  # (r'^api/', include(entry_resource.urls)),

    re_path(r'^i18n/', include('django.conf.urls.i18n')),
 ##  # Json api
 #  url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
 #  url(r'^dajaxice/', include('dajaxice.urls')),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls')),
    ]

#Catch flatpages
urlpatterns += [
    #re_path(r'^', views.flatpage, {'url':'/'}),
    re_path(r'', include('django.contrib.flatpages.urls')),
]

#Catch all
#urlpatterns += [
#    re_path(r'^', views.flatpage),
#]
