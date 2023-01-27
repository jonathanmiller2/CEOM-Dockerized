from ceom.tropomi.models import *
from django.contrib import admin


class TROPOMISingleTimeSeriesJobAdmin(admin.ModelAdmin):
    list_display = ('pixelx', 'pixely', 'result', 'completed', 'user')

admin.site.register(TROPOMISingleTimeSeriesJob, TROPOMISingleTimeSeriesJobAdmin)

class TROPOMIMultipleTimeSeriesJobAdmin(admin.ModelAdmin):
    list_display = ('points', 'result', 'completed', 'user')

admin.site.register(TROPOMIMultipleTimeSeriesJob, TROPOMIMultipleTimeSeriesJobAdmin)

class TROPOMIYearFileAdmin(admin.ModelAdmin):
    list_display = ('year', 'location')

admin.site.register(TROPOMIYearFile, TROPOMIYearFileAdmin)