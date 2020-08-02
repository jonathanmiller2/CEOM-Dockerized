from eomf.visualization.models import *
from django.contrib import admin

class TimeSeriesJobAdmin(admin.ModelAdmin):
    list_display = ('user','sender', 'product', 'timestamp', 'completed','working','error','progress','total_sites','message')

admin.site.register(TimeSeriesJob, TimeSeriesJobAdmin)

class SingleTimeSeriesJobAdmin(admin.ModelAdmin):
    list_display = ('created','user','product','modified', 'completed',)
admin.site.register(SingleTimeSeriesJob, SingleTimeSeriesJobAdmin)