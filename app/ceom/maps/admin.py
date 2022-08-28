from django.contrib import admin
from ceom.maps.models import *

class GeocatterPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'lat', 'lon', 'category')
admin.site.register(GeocatterPoint, GeocatterPointAdmin)