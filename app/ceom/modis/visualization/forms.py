from django import forms
from ceom.modis.visualization.models import TimeSeriesJob
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, Select
import datetime
import os
import csv

class ExtFileField(forms.FileField):
    """
    Same as forms.FileField, but you can specify a file extension whitelist.

    >>> from django.core.files.uploadedfile import SimpleUploadedFile
    >>>
    >>> t = ExtFileField(ext_whitelist=(".pdf", ".txt"))
    >>>
    >>> t.clean(SimpleUploadedFile('filename.pdf', 'Some File Content'))
    >>> t.clean(SimpleUploadedFile('filename.txt', 'Some File Content'))
    >>>
    >>> t.clean(SimpleUploadedFile('filename.exe', 'Some File Content'))
    Traceback (most recent call last):
    ...
    ValidationError: [u'Not allowed filetype!']
    """
    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        self.ext_whitelist = [i.lower() for i in ext_whitelist]

        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ExtFileField, self).clean(*args, **kwargs)
        if data:
            filename = data.name
            ext = os.path.splitext(filename)[1]
            ext = ext.lower()
            if ext not in self.ext_whitelist:
                raise forms.ValidationError("Filetype '%s' not allowed for this field" % ext)
        elif not data and self.required:
            raise forms.ValidationError("Required file not found for %s" % self.label)
        return data

now = datetime.datetime.now()

def makeChoice(a):
    return (str(a), str(a).upper())

PRODUCTS = list(map(makeChoice, ('evi', 'lswi', 'ndsi', 'ndvi', 'ndwi', 'snow')))
DAYS = list(map(makeChoice, list(range(1, 362, 8))))
YEARS = list(map(makeChoice, list(range(2000, now.year+1))))


class TimeSeriesJobForm(forms.ModelForm):
    years = forms.MultipleChoiceField(widget=forms.SelectMultiple,choices=YEARS)
    points = ExtFileField(ext_whitelist=(".txt", ".csv",))

    def clean_years(self):
        data = self.cleaned_data['years']
        return ",".join(data)

    def save_data(self,user,task_id):
        sender =self.cleaned_data["sender"]
        points =self.cleaned_data["points"]
        years =self.cleaned_data["years"]
        product =self.cleaned_data["product"]

        newjob = TimeSeriesJob(sender=sender,points=points,years=years,user=user,product=product,task_id=task_id)
        newjob.save()
        return newjob
    class Meta:
        model = TimeSeriesJob
        fields = ['points','sender',  'product','years']
        #widgets = {            'years': forms.SelectMultiple(choices=YEARS),        }
