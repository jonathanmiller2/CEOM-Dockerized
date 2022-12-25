from ceom.modis.models import *
from django.contrib import admin

class DatasetAdmin(admin.ModelAdmin):
	list_display = ('name', 'grid_name', 'long_name','day_res','xdim','ydim','is_global')
	
admin.site.register(Dataset, DatasetAdmin)

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'long_name')

admin.site.register(Product, ProductAdmin)