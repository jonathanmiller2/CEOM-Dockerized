from eomf.geohealth.models import *
from django.contrib import admin

class DatainfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'fullname', 'label', 'datatype', 'source', 'order')

admin.site.register(H5n1)
admin.site.register(Birds)
admin.site.register(Datatype)
admin.site.register(Datainfo, DatainfoAdmin)
