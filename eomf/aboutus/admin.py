from models import Post, PostImage, PostFile, Group, Person, GalleryPhoto
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from tinymce.widgets import TinyMCE
from django.http import HttpResponse

class PostImageInLine(admin.StackedInline):
    model = PostImage
    extra = 2
class PostFileInLine(admin.StackedInline):
    model = PostFile
    extra = 2

class PostAdmin(admin.ModelAdmin):
    list_filter = ['date']
    list_display = ('title','date','content',)
    fieldsets = [
        ('Post data',  {'fields': ['title','date', 'content','image_comlumn_number']}),
    ]
    inlines = [PostImageInLine,PostFileInLine]
    class Meta:
        model = Post
        
admin.site.register(Post, PostAdmin)

class PersonAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'middle_name', 'last_name', 'title', 'group', 'link','date')
	list_filter = ['date']
	search_fields = ['title']
	date_hierarchy = 'date'

class GroupAdmin(admin.ModelAdmin):
	list_display = ('name','order')

class GalleryPhotoAdmin(admin.ModelAdmin):
	list_filter = ['year']
	search_fields = ['title']
	list_display = ('year','order','title','description','picture')
	
admin.site.register(GalleryPhoto, GalleryPhotoAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)

