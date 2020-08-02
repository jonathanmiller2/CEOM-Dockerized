from django import forms
from django.forms import ModelForm

from models import Research
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import datetime
import os
from django.contrib.auth.models import User

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

class AddPixelToResearchForm(forms.Form):
    research = forms.ModelChoiceField(queryset=Research.objects.all()) # Or whatever query you'd like
    points = ExtFileField(ext_whitelist=(".txt", ".csv",))

class ResearchForm(forms.ModelForm):
    user = None
    def __init__(self, *args, **kwargs):
        super(ResearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
    class Meta:
        model = Research
        fields = ['name','description',]
    def set_user(self, user):
        self.user = user
    def clean_name(self):
        a = self.cleaned_data.keys()
        user = self.user
        if not user:
            raise forms.ValidationError("No user selected. Make sure that you are logged in")
        name = self.cleaned_data["name"]
        try:
            name = self.cleaned_data["name"]
            obj = Research.objects.get(user=user,name=name)
            raise forms.ValidationError("Research name already exists in your list")
        except:
            pass
        return name
            

class ResearchFormEdit(forms.ModelForm):
    user = None

    def __init__(self, *args, **kwargs):
        super(ResearchFormEdit, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
    class Meta:
        model = Research
        fields = ['name','description',]
    def set_user(self, user):
        self.user = user
    def set_id(self, id):
        self.id = id
    