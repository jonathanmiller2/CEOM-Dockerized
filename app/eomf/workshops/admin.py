# from django.contrib.gis import admin
from eomf.workshops.models import *
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from tinymce.widgets import TinyMCE
import csv
from django.http import HttpResponse


def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')
        
        writer = csv.writer(response)
        if header:
            writer.writerow(list(field_names))
        for obj in queryset:
            writer.writerow([str(getattr(obj, field)).encode('utf-8') for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv


class WorkshopClassAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ['name',]
admin.site.register(WorkshopClass, WorkshopClassAdmin)

class SponsorInWorkshopInline(admin.StackedInline):
    model = SponsorInWorkshop
    extra = 2

class PresentationInWorkshopInline(admin.StackedInline):
    model = Presentation
    extra = 2

class WorkshopPhotoInlineAdmin(admin.TabularInline):
    model = WorkshopPhoto
    extra = 2

# class WorkshopAdmin(admin.ModelAdmin):
#     list_display = ("name","date_start","date_end",'category')
#     search_fields = ['name', 'date_start']
#     inlines = [PresentationInWorkshopInline,SponsorInWorkshopInline,WorkshopPhotoInlineAdmin]
# admin.site.register(Workshop, WorkshopAdmin)

class WorkshopRegistrationAdmin(admin.ModelAdmin):
    list_display = ("last_name","first_name",'email','institution','workshop','validated','address','phone','extra_text_field1','extra_text_field2','extra_text_field3','extra_boolean_field1','extra_boolean_field2','extra_boolean_field3')
    list_filter = ['workshop','institution']
    #search_fields = ['workshop','last_name','first_name']
    actions = [export_as_csv_action("Export selected sponsors to CSV", fields= list_display, header=True),]
    readonly_fields = ("created","modified",)
admin.site.register(WorkshopRegistration, WorkshopRegistrationAdmin)

class SponsorAdmin(admin.ModelAdmin):
    list_display = ("name",)
admin.site.register(Sponsor, SponsorAdmin)

class PresentationAdmin(admin.ModelAdmin):
    list_display = ("workshop","first_name","last_name","other_presenters","time_ini","time_end")
    search_fields = ['workshop','last_name','first_name']
    readonly_fields = ("created","modified",)
admin.site.register(Presentation, PresentationAdmin)

class WorkshopPhotoAdmin(admin.ModelAdmin):
    list_display = ("workshop","priority","image","created","modified")
    search_fields = ['workshop','image',"created","modified"]
    readonly_fields = ("created","modified",)
admin.site.register(WorkshopPhoto, WorkshopPhotoAdmin)

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name","link")
    search_fields = ['name',]
    readonly_fields = ("created","modified",)
admin.site.register(Institution, InstitutionAdmin)


class GalleryMultiuploadMixing(object):

    def process_uploaded_file(self, uploaded, workshop, request):
        try:
            if workshop:
                image = WorkshopPhoto(workshop=workshop,image=uploaded)
                image.save()
            return {
                'url': image.image.url,
                'thumbnail_url': image.image.url,
                'id': image.id,
                'name': image.filename
            }
        except Exception as e:
            return {
                'url': 'url',
                'thumbnail_url': 'thumbnail_url',
                'id': -1,
                'name': e.message
            }


#TODO: I'm removing some multiupload stuff, because it needs to be replaced with Django's multiple file upload handler (https://docs.djangoproject.com/en/2.2/topics/http/file-uploads/)
#Unfortunately this means this will probably break at some point
class GalleryAdmin(admin.ModelAdmin, GalleryMultiuploadMixing):
    inlines = [WorkshopPhotoInlineAdmin,]
    multiupload_form = True
    multiupload_list = False

    def delete_file(self, pk, request):
        '''
        Delete an image.
        '''
        obj = get_object_or_404(Image, pk=pk)
        return obj.delete()


class ImageAdmin(GalleryMultiuploadMixing):
    multiupload_form = False
    multiupload_list = True


admin.site.register(Workshop, GalleryAdmin)
# admin.site.register(Image, ImageAdmin)