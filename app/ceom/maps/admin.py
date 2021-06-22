from django.contrib import admin

from ceom.maps.models import map_gallery, Comment, poi, roi


class CommentInline(admin.TabularInline):
	model = Comment

class map_galleryAdmin(admin.ModelAdmin):
	inlines = [
		CommentInline,
	]

admin.site.register(map_gallery, map_galleryAdmin)


class poiAdmin(admin.ModelAdmin):
	pass

admin.site.register(poi, poiAdmin)


class roiAdmin(admin.ModelAdmin):
	pass

admin.site.register(roi, roiAdmin)
# vim: et sw=4 sts=4
