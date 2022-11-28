from ceom.modis.models import *
from django.contrib import admin

class DatasetAdmin(admin.ModelAdmin):
	list_display = ('name', 'grid_name', 'long_name','day_res','xdim','ydim','is_global')
	
admin.site.register(Dataset, DatasetAdmin)

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'long_name')

admin.site.register(Product, ProductAdmin)

class MODISMultipleTimeSeriesJobAdmin(admin.ModelAdmin):
    list_display = ('user','sender', 'product', 'timestamp', 'completed','working','error','progress','total_sites','message')

admin.site.register(MODISMultipleTimeSeriesJob, MODISMultipleTimeSeriesJobAdmin)

class MODISSingleTimeSeriesJobAdmin(admin.ModelAdmin):
    list_display = ('created','user','product','modified', 'completed',)
admin.site.register(MODISSingleTimeSeriesJob, MODISSingleTimeSeriesJobAdmin)