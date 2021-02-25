from ceom.inventory.models import *
from django.contrib import admin

class DatasetAdmin(admin.ModelAdmin):
	# fieldsets = [
	# 	(None, {'fields': ['name']}),
	# 	(None, {'fields': ['grid_name']}),
	# 	(None, {'fields': ['long_name']}),
	# 	(None, {'fields': ['short_name']}),
	# 	(None, {'fields': ['xdim']}),
	# 	(None, {'fields': ['ydim']}),
	# 	(None, {'fields': ['grid_size']}),
	# 	(None, {'fields': ['projcode']}),
	# 	(None, {'fields': ['zonecode']}),
	# 	(None, {'fields': ['spherecode']}),
	# 	(None, {'fields': ['projparm']}),
	# 	(None, {'fields': ['ordering']}),
	# ]
	list_display = ('name', 'grid_name', 'long_name','day_res','xdim','ydim','is_global')
	
admin.site.register(Dataset, DatasetAdmin)

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'long_name')

admin.site.register(Product, ProductAdmin)

class TileAdmin(admin.ModelAdmin):
    list_display = ('name','continent', 'lon_min', 'lon_max', 'lat_min', 'lat_max')

admin.site.register(Tile, TileAdmin)
admin.site.register(File)
