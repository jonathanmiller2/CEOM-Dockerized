from django import forms
import eomf.eomfshare.models

class UploadFileForm(forms.ModelForm):
    # title = forms.CharField(max_length=50)
    # file = forms.FileField()
    class Meta:
        model = eomf.eomfshare.models.uploadfile
        fields = ['FileNew']