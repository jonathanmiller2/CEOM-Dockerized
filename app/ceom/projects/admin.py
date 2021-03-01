from ceom.projects.models import Project
from django.contrib import admin

class ProjAdmin(admin.ModelAdmin):
    list_display = ('project_title','funding_agency','start_date','end_date','fund')
    list_filter = ['end_date']
    search_fields = ['project_title']
    date_hierarchy = 'end_date'


admin.site.register(Project, ProjAdmin)