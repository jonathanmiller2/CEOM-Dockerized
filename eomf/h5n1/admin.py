from django.contrib.gis import admin
from eomf.h5n1.models import Case

admin.site.register(Case, admin.GeoModelAdmin)
