from django.urls import path
from django.conf.urls import url, include
from filebrowser.sites import site
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect


from django.contrib.staticfiles.urls import staticfiles_urlpatterns #For dajaxice
urlpatterns = [
    path('^grappelli/', include('grappelli.urls')),
    path('^admin/', admin.site.urls),
    path('^admin/filebrowser/', site.urls),
    
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^captcha/', include('captcha.urls')),

    url(r'^accounts/', include('eomf.accounts.urls')),
    url(r'^modis/visualization/',include('eomf.visualization.urls')),
    url(r'^visualization/',include('eomf.visualization.urls')),
    url(r'^modis/data/',include('eomf.inventory.urls')),
    url(r'^inventory/',include('eomf.inventory.urls')),
    url(r'^data/',include('eomf.inventory.urls')),
    url(r'^geohealth/', include('eomf.geohealth.urls')),
    url(r'^photos/', include('eomf.photos.urls')),
    url(r'^birds/', include('eomf.birds.urls')),
    url(r'^h5n1/', include('eomf.h5n1.urls')),
 ##   # url(r'^service/', include('eomf.data.urls')),
    url(r'^gisday/', include('eomf.gisday.urls')),
    url(r'^contact/', TemplateView.as_view(template_name="contact.html")),
    url(r'^projects/', include('eomf.projects.urls')),
    url(r'^aboutus/',include('eomf.aboutus.urls')),
    url(r'^workshops/',include('eomf.workshops.urls')),
    url(r'^stats/', include('eomf.stats.urls')),
    url(r'^towers/', include('eomf.towers.urls')),
    url(r'^feedback/', include('eomf.feedback.urls')),
    url(r'^share/', include('eomf.eomfshare.urls')),
    url(r'^maps/', include('eomf.maps.urls')),
    url(r'^water/', include('eomf.water.urls')),
    # (r'^aoitest/', include('eomf.aoitest.urls')),
 ##   # (r'^poi/', include('eomf.poi.urls')),
 ##  # (r'^api/', include(entry_resource.urls)),

    url(r'^i18n/', include('django.conf.urls.i18n')),
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
        url(r'^rosetta/', include('rosetta.urls')),
    ]
#Catch all
urlpatterns.append( url(r'^', include('eomf.pages.urls')) )
#urlpatterns += staticfiles_urlpatterns()
# urlpatterns += staticfiles_urlpatterns()
