from django.urls import path, re_path
from django.conf.urls import url, include
from filebrowser.sites import site
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    re_path('^grappelli/', include('grappelli.urls')),
    re_path('^admin/', admin.site.urls),
    re_path('^admin/filebrowser/', site.urls),
    
    re_path(r'^tinymce/', include('tinymce.urls')),
    re_path(r'^captcha/', include('captcha.urls')),

    re_path(r'^accounts/', include('ceom.accounts.urls')),
    re_path(r'^modis/visualization/',include('ceom.modis.visualization.urls')),
    re_path(r'^visualization/',include('ceom.modis.visualization.urls')),
    re_path(r'^modis/data/',include('ceom.modis.inventory.urls')),
    re_path(r'^inventory/',include('ceom.modis.inventory.urls')),
    re_path(r'^data/',include('ceom.modis.inventory.urls')),
    re_path(r'^geohealth/', include('ceom.geohealth.urls')),
    re_path(r'^photos/', include('ceom.photos.urls')),
    re_path(r'^birds/', include('ceom.birds.urls')),
    re_path(r'^h5n1/', include('ceom.h5n1.urls')),
    re_path(r'^contact/', TemplateView.as_view(template_name="contact.html")),
    re_path(r'^aboutus/',include('ceom.aboutus.urls')),
    re_path(r'^outreach/workshops/', include('ceom.outreach.workshops.urls')),
    re_path(r'^outreach/gisday/', include('ceom.outreach.gisday.urls')),
    re_path(r'^stats/', include('ceom.stats.urls')),
    re_path(r'^towers/', include('ceom.towers.urls')),
    re_path(r'^maps/', include('ceom.maps.urls')),
    re_path(r'^water/', include('ceom.water.urls')),
    re_path(r'^poi/', include('ceom.poi.urls')),
    url(r'^raster/', include('raster.urls')),
]

urlpatterns += [
    re_path(r'', include('django.contrib.flatpages.urls')),
]
