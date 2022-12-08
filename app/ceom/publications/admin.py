from ceom.aboutus.models import Category
from ceom.aboutus.models import Publication
from django.contrib import admin


class PubAdmin(admin.ModelAdmin):
	list_display = ('title', 'date', 'authorship', 'pubtype', 'category')
	list_filter = ['date']
	search_fields = ['title']
	date_hierarchy = 'date'

class CatAdmin(admin.ModelAdmin):
	list_display = ('name',)
	
admin.site.register(Publication, PubAdmin)
