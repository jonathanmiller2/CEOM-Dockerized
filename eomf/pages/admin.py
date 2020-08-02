from django import forms
from django.contrib import admin
from eomf.pages.models import ContentPage
from django.utils.translation import ugettext_lazy as _
from tinymce.widgets import TinyMCE

class ContentpageForm(forms.ModelForm):
    #content = forms.CharField(widget=openWYSIWYG(attrs={'rows':'100', 'style':'width:94%;height:800px;'}))
    content = forms.CharField(widget=TinyMCE(
                attrs={'rows':30, 'cols':60}#, mce_attrs={'height':"800"}
            ))
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/]+$',
        help_text = _("Example: '/about/contact/'. Make sure to have leading"
                      " and trailing slashes."))

    class Meta:
        model = ContentPage
        fields = '__all__'

class ContentPageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'template_name')}),
    )
    list_display = ('url', 'title')
    list_filter = ('sites', 'enable_comments', 'registration_required')
    search_fields = ('url', 'title')
    form = ContentpageForm

    #class Media:
    #    js = ('/static/pages_admin.js',)
        
admin.site.register(ContentPage, ContentPageAdmin)
