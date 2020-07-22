from django import forms
import models

class UploadFileForm(forms.ModelForm):
    # title = forms.CharField(max_length=50)
    # file = forms.FileField()
    class Meta:
        model = models.uploadfile
        fields = ['FileNew']