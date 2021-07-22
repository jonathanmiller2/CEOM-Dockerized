from ceom.modis.inventory.models import *
from django.contrib import admin

class DatasetAdmin(admin.ModelAdmin):
	list_display = ('name', 'grid_name', 'long_name','day_res','xdim','ydim','is_global')
	
admin.site.register(Dataset, DatasetAdmin)

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'long_name')

admin.site.register(Product, ProductAdmin)

class TileAdmin(admin.ModelAdmin):
    list_display = ('name','continent', 'lon_min', 'lon_max', 'lat_min', 'lat_max')

admin.site.register(Tile, TileAdmin)
admin.site.register(File)
