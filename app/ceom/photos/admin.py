from django.contrib.gis import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from ceom.photos.models import *

class CategoryAdmin(admin.GeoModelAdmin):
    actions = None

admin.site.register(Category, CategoryAdmin)

def status_deleted(modeladmin, request, queryset):
    queryset.update(status=0)
status_deleted.short_description = "Set status: Deleted"
def status_public(modeladmin, request, queryset):
    queryset.update(status=1)
status_public.short_description = "Set status: Public"
def status_private(modeladmin, request, queryset):
    queryset.update(status=2)
status_private.short_description = "Set status: Private"

class PhotoAdmin(admin.GeoModelAdmin):
    list_display = ("id", "file","user","uploaddate","takendate","status")
    exclude = ("file_hash","source","_lon","_lat","datum","regionid",)
    actions = [status_deleted, status_public, status_private]
    search_fields = ['user__email', 'user__username']

admin.site.register(Photo, PhotoAdmin)
