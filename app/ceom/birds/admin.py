from django.contrib.gis import admin
from ceom.birds.models import DuckTrack, DuckTrackLine

admin.site.register(DuckTrack, admin.GeoModelAdmin)
admin.site.register(DuckTrackLine, admin.GeoModelAdmin)
