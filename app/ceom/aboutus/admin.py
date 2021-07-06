from ceom.aboutus.models import Post, PostImage, Person, GalleryPhoto, Category
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from tinymce.widgets import TinyMCE
from django.http import HttpResponse
from django.core.exceptions import FieldError

class PostImageInLine(admin.StackedInline):
    model = PostImage
    extra = 2

class PostAdmin(admin.ModelAdmin):
    list_filter = ['date']
    list_display = ('title','date','content',)
    fieldsets = [
        ('Post data',  {'fields': ['title','date', 'content','image_column_number']}),
    ]
    inlines = [PostImageInLine]
    class Meta:
        model = Post
        
admin.site.register(Post, PostAdmin)

class PersonAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'middle_name', 'last_name', 'title', 'category', 'date')
	list_filter = ['date']
	search_fields = ['title']
	date_hierarchy = 'date'

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name','order')

class GalleryPhotoAdmin(admin.ModelAdmin):
	list_filter = ['year']
	search_fields = ['title']
	list_display = ('year','order','title','description','picture')
	
admin.site.register(GalleryPhoto, GalleryPhotoAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Category, CategoryAdmin)

