import datetime
from django import forms
# Olwidget not working on django 1.8
# from olwidget.forms import MapModelForm
from django.contrib.auth.models import User
from models import Photo, Category
from models import ContinentBuffered, CountryBuffered
from django.forms.extras.widgets import SelectDateWidget, Select
from django.utils.translation import ugettext_lazy as _

from models import DIR_CARD_CHOICES

category_qs = Category.objects.order_by("order").all()
users = Photo.objects.values('user').distinct()
user_qs = User.objects.filter(id__in=users).order_by("username").all()
country_qs = CountryBuffered.objects.order_by("name").all()
continent_qs = ContinentBuffered.objects.order_by("name").all()
dmin = datetime.datetime(1990, 1, 1)
dmax = datetime.date.today()


class BatchEditForm(forms.Form):
    status = forms.TypedChoiceField(
        choices=(
            ('', '(Not Changed)'),
            (0, 'Deleted',),
            (1, 'Public',),
            (2, 'Private',)
        ),
        initial='(Not Changed)', required = False
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="(Not Changed)", required=False
    )
    feild_notes = forms.CharField(widget=forms.Textarea, required=False)


class SearchForm(forms.Form):
    lon_min = forms.FloatField(max_value=180, min_value=-180, required=False)
    lon_max = forms.FloatField(max_value=180, min_value=-180, required=False)
    lat_min = forms.FloatField(max_value=90, min_value=-90, required=False)
    lat_max = forms.FloatField(max_value=90, min_value=-90, required=False)
    address_get = forms.CharField(max_length=1600, required=False)
    LAT_DEG = forms.FloatField(max_value=90, min_value=-90, required=False)
    LAT_MIN = forms.FloatField(max_value=60, min_value=0, required=False)
    LAT_SEC = forms.FloatField(max_value=60, min_value=0, required=False)
    LAT_DEG1 = forms.FloatField(max_value=180, min_value=-180, required=False)
    LON_DEG = forms.FloatField(max_value=180, min_value=-180, required=False)
    LON_MIN = forms.FloatField(max_value=60, min_value=0, required=False)
    LON_SEC = forms.FloatField(max_value=60, min_value=0, required=False)
    LON_DEG1 = forms.FloatField(max_value=180, min_value=-180, required=False)
    precise = forms.FloatField(max_value=30, min_value=-30, required=False)
    date_min = forms.DateField(
        initial=None, required=False,
        widget=forms.DateInput(format='%m/%d/%Y', attrs={'class': 'span12','placeholder':'mm/dd/yyyy'}),
        input_formats=('%m/%d/%Y', '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d')
    )

    date_max = forms.DateField(
        initial=None, required=False,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'span12','placeholder':'mm/dd/yyyy'}),        
        input_formats=('%m/%d/%Y', '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d')
    )

    category = forms.ModelChoiceField(
        queryset=category_qs,
        required=False,
        empty_label=_("All"),
        widget=Select(
            attrs={'class': 'span12'},
            choices=(('notnull', 'Is Set'), ('null', 'Not Set'))
        )
    )


    user = forms.CharField(
        max_length=50,
        required=False,
        widget = forms.TextInput(
            attrs={'class': 'span12'}
        )
    )

    country = forms.ModelChoiceField(
        queryset=country_qs,
        required=False,
        empty_label=_("All"),
        widget=Select(
            attrs={'class': 'span12'},
            choices=(('notnull', 'Is Set'), ('null', 'Not Set'))
        )
    )

    continent = forms.ModelChoiceField(
        queryset=continent_qs,
        required=False,
        empty_label=_("All"),
        widget=Select(
            attrs={'class': 'span12'},
            choices=(('notnull', 'Is Set'), ('null', 'Not Set'))
        )
    )

    keywords = forms.CharField(max_length=255, required=False)
    
    def clean_user(self):
        user_name = self.cleaned_data["user"]
        user = None
        try:
            user = User.objects.get(username=user_name)
        except:
            pass
        return user

class WorksetForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("category", "notes", "status")





class PhotoForm(forms.ModelForm):
    lon = forms.FloatField(required=False, help_text="use +/- to designate east or west hemisphere")
    lat = forms.FloatField(required=False, help_text="use +/- to designate east or west hemisphere")

    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)

        # Set the form fields based on the model object
        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.initial['lat'] = instance.lat
            self.initial['lon'] = instance.lon

            #WTF - form.instance gets padded with spaces and breaks select
            if instance.dir_card:
               self.initial['dir_card'] = self.initial['dir_card'].strip()


    def save_off(self, commit=True):
        model = super(PhotoForm, self).save(commit=False)

        # Save the latitude and longitude based on the form fields
        model.lat = self.cleaned_data['lat']
        model.lon = self.cleaned_data['lon']

        if commit:
            model.save()

        return model

    class Meta:
        model = Photo
        options = {'layers': ['google.hybrid'], 'map_div_style': {'width': '400px', 'height': '300px'}}
        fields = ("point", "alt", "takendate", "dir_card", "category", "notes", "status")
