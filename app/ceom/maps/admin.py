from django.contrib import admin
from ceom.maps.models import *

class GeocatterPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_categorized', 'date_taken', 'grid_npix', 'tile_h', 'tile_v', 'pixel_x', 'pixel_y', 'is_multi_cat', 'primary_category', 'secondary_category')
admin.site.register(GeocatterPoint, GeocatterPointAdmin)