from ceom.outreach.gisday.models import *
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


class YearAdmin(admin.ModelAdmin):
    list_filter = ['date']
    list_display = ('date','registration_closed','address','hidden','time_ini','time_end','summary_hidden','agenda_hidden','photo_contest_hidden','poster_contest_hidden','image_gallery_hidden','photo_gallery_hidden','survey_open')
    actions = [export_as_csv_action("Export selected booths to CSV", fields= list_display, header=True),]
    class Meta:
        model = Year
        
admin.site.register(Year, YearAdmin)


class BoothAdmin(admin.ModelAdmin):
    list_filter = ['last_name','year']
    list_display = ('year','last_name','first_name','non_profit','institution','department','address_1','address_2','city','state','zipcode','phone','email','names','tshirt_size_1','tshirt_size_2','comment','permits','oversized','comment','validated')
    actions = [export_as_csv_action("Export selected booths to CSV", fields= list_display, header=True),]
    class Meta:
        model = Booth
        
admin.site.register(Booth, BoothAdmin)

class VisitorAdmin(admin.ModelAdmin):
    list_filter = ['last_name','year']
    list_display = ("last_name","year","first_name", "email","institution", "created","validated", "comment")
    actions = [export_as_csv_action("Export selected visitors to CSV", fields= list_display, header=True),]
    class Meta:
        model = Visitor
        
admin.site.register(Visitor, VisitorAdmin)

class PhotoContestParticipantAdmin(admin.ModelAdmin):
    list_filter = ['last_name','year']
    list_display = ("last_name", "first_name", "email","comment","validated")
    actions = [export_as_csv_action("Export selected photo contest participants to CSV", fields= list_display, header=True),]
    class Meta:
        model = PhotoContestParticipant
        
admin.site.register(PhotoContestParticipant, PhotoContestParticipantAdmin)

class PosterCategoryAdmin(admin.ModelAdmin):
    list_filter = ['name',]
    list_display = ('name',"description",)
    actions = [export_as_csv_action("Export selected poster contest categories participants to CSV", fields= list_display, header=True),]
    class Meta:
        model = PosterCategory
admin.site.register(PosterCategory, PosterCategoryAdmin)    

class PosterAdmin(admin.ModelAdmin):
    list_filter = ['last_name','year']
    list_display = ('year',"last_name", "first_name","category", "email","comment","validated","preview")
    actions = [export_as_csv_action("Export selected poster contest participants to CSV", fields= list_display, header=True),]
    class Meta:
        model = Poster


admin.site.register(Poster, PosterAdmin)

class AboutUsGroupAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ("name", "order")
    class Meta:
        model = AboutUsGroup
admin.site.register(AboutUsGroup, AboutUsGroupAdmin)   
    
class AboutUsPersonAdmin(admin.ModelAdmin):
    list_filter = ['last_name']
    list_display = ("last_name", "first_name","middle_name", "email","phone","headshot")
    actions = [export_as_csv_action("Export selected persons to CSV", fields= list_display, header=True),]
    class Meta:
        model = AboutUsPerson
admin.site.register(AboutUsPerson, AboutUsPersonAdmin)

class PersonInGroupAdmin(admin.ModelAdmin):
    list_filter = ['person','year']
    list_display = ('year',"person","group","year", "highlight")
    class Meta:
        model = PersonInGroup
admin.site.register(PersonInGroup, PersonInGroupAdmin)

class SponsorCategoryAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ("name","min_inversion","max_inversion","logo")
    class Meta:
        model = SponsorCategory
admin.site.register(SponsorCategory, SponsorCategoryAdmin)


class SponsorAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ("name","link","contact_person_name","contact_person_phone","contact_person_mail")
    actions = [export_as_csv_action("Export selected sponsors to CSV", fields= list_display, header=True),]
    class Meta:
        model = Sponsor
admin.site.register(Sponsor, SponsorAdmin)

class SponsorInYearAdmin(admin.ModelAdmin):
    list_filter = ['year','sponsor','category']
    list_display = ("year","sponsor","money",'category',)
    actions = [export_as_csv_action("Export selected sponsors to CSV", fields= list_display, header=True),]
    class Meta:
        model = SponsorInYear
admin.site.register(SponsorInYear, SponsorInYearAdmin)

class ItemDonorAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ("name","link",)
    actions = [export_as_csv_action("Export selected item donor/s to CSV", fields= list_display, header=True),]
    class Meta:
        model = ItemDonor
admin.site.register(ItemDonor, ItemDonorAdmin)   
    
class ItemInYearAdmin(admin.ModelAdmin):
    list_filter = ['year']
    list_display = ("year","name", "donor","value","link")
    actions = [export_as_csv_action("Export selected items to CSV", fields= list_display, header=True),]
    class Meta:
        model = ItemInYear
admin.site.register(ItemInYear, ItemInYearAdmin)

class GisDayPhotoAdmin(admin.ModelAdmin):
    list_filter = ['year','id']
    list_display = ('year','id','picture')
    class Meta:
        model = GisDayPhoto
admin.site.register(GisDayPhoto, GisDayPhotoAdmin)


class AgendaAdmin(admin.ModelAdmin):
    list_filter = ['year','entry_name']
    list_display = ('year','entry_name','time_ini',"time_end","speaker")
    class Meta:
        model = Agenda
admin.site.register(Agenda, AgendaAdmin)


class AnnouncementAdmin(admin.ModelAdmin):
    list_filter = ['year','entry_name']
    list_display = ('year','position','entry_name',"date")
    class Meta:
        model = Announcement
admin.site.register(Announcement, AnnouncementAdmin)


class SummaryContentAdmin(admin.ModelAdmin):
    list_filter = ['year',]
    list_display = ('year',)
    class Meta:
        model = SummaryContent
admin.site.register(SummaryContent, SummaryContentAdmin)

class PosterContestContentAdmin(admin.ModelAdmin):
    list_filter = ['year',]
    list_display = ('year',)
    class Meta:
        model = PosterContestContent
admin.site.register(PosterContestContent, PosterContestContentAdmin)

class PhotoContestContentAdmin(admin.ModelAdmin):
    list_filter = ['year',]
    list_display = ('year',)
    class Meta:
        model = PhotoContestContent
admin.site.register(PhotoContestContent, PhotoContestContentAdmin)

class LogisticsContentAdmin(admin.ModelAdmin):
    list_filter = ['year',]
    list_display = ('year',)
    class Meta:
        model = LogisticsContent
admin.site.register(LogisticsContent, LogisticsContentAdmin)


class VisitorRegistrationContentAdmin(admin.ModelAdmin):
    list_filter = ['year',]
    list_display = ('year',)
    class Meta:
        model = VisitorRegistrationContent
admin.site.register(VisitorRegistrationContent, VisitorRegistrationContentAdmin)


class SponsorsContentAdmin(admin.ModelAdmin):
    list_filter = ['year',]
    list_display = ('year',)
    class Meta:
        model = SponsorsContent
admin.site.register(SponsorsContent, SponsorsContentAdmin)


class CommitteeContentAdmin(admin.ModelAdmin):
    list_filter = ['year',]
    list_display = ('year',)
    class Meta:
        model = CommitteeContent
admin.site.register(CommitteeContent, CommitteeContentAdmin)

class BoothContentAdmin(admin.ModelAdmin):
    list_filter = ['year',]
    list_display = ('year','max_booths')
    class Meta:
        model = BoothContent

admin.site.register(BoothContent, BoothContentAdmin)

class SurveyAdmin(admin.ModelAdmin):
    list_filter = ['year','role','institution','position','gender','highest_degree','highest_degree','ethnicity','citizenship','race','disability','parents_degree']
    list_display = ('year','role','institution','position','gender','highest_degree','highest_degree','ethnicity','citizenship','race','disability','parents_degree')
    readonly_fields=('created','modified',)
    actions = [export_as_csv_action("Export selected item donor/s to CSV", fields= list_display, header=True),]
    class Meta:
        model = Survey
    
admin.site.register(Survey, SurveyAdmin)

class DemographicSurveyAdmin(admin.ModelAdmin):
    list_filter = ['year','institution','position','gender','highest_degree','highest_degree','ethnicity','citizenship','race','disability','parents_degree']
    list_display = ('year','institution','position','gender','highest_degree','highest_degree','ethnicity','citizenship','race','disability','parents_degree')
    readonly_fields=('created','modified',)
    actions = [export_as_csv_action("Export selected item donor/s to CSV", fields= list_display, header=True),]
    class Meta:
        model = DemographicSurvey
    
admin.site.register(DemographicSurvey, DemographicSurveyAdmin)

class SurveyContentsAdmin(admin.ModelAdmin):
    list_filter = ['year',]
    list_display = ('year','content',)
    actions = [export_as_csv_action("Export selected item donor/s to CSV", fields= list_display, header=True),]
    class Meta:
        model = SurveyContents

admin.site.register(SurveyContents, SurveyContentsAdmin)
