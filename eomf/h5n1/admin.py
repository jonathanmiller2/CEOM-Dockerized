from django.contrib.gis import admin
from models import Case

admin.site.register(Case, admin.GeoModelAdmin)
