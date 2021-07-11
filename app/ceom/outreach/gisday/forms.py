from django.forms import ModelForm
from django.db import models
from django import forms
from ceom.outreach.gisday.models import Booth, Visitor, PhotoContestParticipant, Poster, Year
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Layout, Field, Row, Div, Column, Fieldset

#capchta
from captcha.fields import CaptchaField
#from simplemathcaptcha.fields import MathCaptchaField

class BoothForm(ModelForm):
    captcha = CaptchaField()
    #captcha = MathCaptchaField()
    non_profit = forms.TypedChoiceField(
        coerce=lambda x: True if x == 'True' else False,
        choices=(
            (True, 'University / Government / Non-Profit: Free registration'),
            (False, 'Private Industry / For Profit: $300 registration fee')
        ),
        widget=forms.RadioSelect(attrs={"class": "unstyled"}),
        label="Institution Type"
    )

    def __init__(self, *args, **kwargs):
        super(BoothForm, self).__init__(*args, **kwargs)
        self.fields['verifyemail'] = forms.EmailField(label="verify email",required=True, max_length=60)
        self.fields['year']=forms.ModelChoiceField(queryset=Year.objects.all(), widget=forms.HiddenInput())
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Div('year',
                Div('form_errors', style="font-size: 25px; font-weight: bold;",css_class="span12"),
                Div('non_profit', style="font-size: 25px; font-weight: bold;",css_class="span12"),
                Div(Div('institution', style="font-size: 25px; font-weight: bold;",css_class="span6"), Div('department',style="font-size: 25px; font-weight: bold;",css_class="span6"),css_class='span12'),
                Div(Div('last_name', style="font-size: 25px; font-weight: bold;",css_class="span6"), Div('first_name',style="font-size: 25px; font-weight: bold;",css_class="span6"),css_class='span12'),
                Div(Div('address_1',style="font-size: 25px; font-weight: bold;",css_class="span6"), Div('address_2',style="font-size: 25px; font-weight: bold;",css_class="span6"),css_class='span12'),
                Div(Div('city',style="font-size: 25px; font-weight: bold;",css_class="span6"), Div('state',style="font-size: 25px; font-weight: bold;",css_class="span6"),css_class='span12'),
                Div(Div('zipcode',style="font-size: 25px; font-weight: bold;",css_class="span6"), Div('phone',style="font-size: 25px; font-weight: bold;",css_class="span6"),css_class='span12'),
                Div(Div('email',style="font-size: 25px; font-weight: bold;",css_class="span6"), Div('verifyemail',style="font-size: 25px; font-weight: bold;",css_class="span6"),css_class='span12'),
                Div(Div('tshirt_size_1',style="font-size: 25px; font-weight: bold;",css_class="span6"), Div('tshirt_size_2',style="font-size: 25px; font-weight: bold;",css_class="span6"),css_class='span12'),
                Div(Div('names',style="font-size: 25px; font-weight: bold;",css_class="span6"), Div('comment',style="font-size: 25px; font-weight: bold;",css_class="span6"),css_class='span12'),
                Div(Div('permits',style="font-size: 25px; font-weight: bold;",css_class="span6"), Div('oversized',style="font-size: 25px; font-weight: bold;",css_class="span6"),css_class='span12'),
                Div(Div(Field('captcha', placeholder=" Enter Result"),style="font-size: 25px; font-weight: bold;",css_class="span12"), css_class='span12'),
           ),
        )

    class Meta:
        model = Booth
        exclude = ("created", "modified", "validated")

    def clean_verifyemail(self):
        try:
            email = self.cleaned_data['email']
        except:
            raise forms.ValidationError("Above email in wrong format")
        verifyemail = self.cleaned_data['verifyemail']
        if email != verifyemail:
            raise forms.ValidationError("Emails do not match")
        return verifyemail


class VisitorForm(ModelForm):
    captcha = CaptchaField()
    #captcha = MathCaptchaField()
    # year= models.DateTimeField(widget=widgets.HiddenInput)
    def __init__(self, *args, **kwargs):
        super(VisitorForm, self).__init__(*args, **kwargs)
        self.fields['verifyemail'] = forms.EmailField(label="verify email",required=True, max_length=60)
        self.fields['year']=forms.ModelChoiceField(queryset=Year.objects.all(), widget=forms.HiddenInput())
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        #self.fields['captcha'] = forms.CharField(widget = forms.TextInput(attrs={'placeholder': 'Enter Result'}))
        self.fields.keyOrder =['year','last_name', 'first_name', 'email', 'verifyemail', 'institution', 'comment','captcha','test']
    class Meta:
        model = Visitor
        exclude = ("created", "modified","validated")

    def clean_verifyemail(self):
        try:
            email = self.cleaned_data['email']
        except:
            raise forms.ValidationError("Above email in wrong format")
        verifyemail = self.cleaned_data['verifyemail']
        if email != verifyemail:
            raise forms.ValidationError("Emails do not match")
        return verifyemail

class PhotoForm(ModelForm):
    captcha = CaptchaField()
    #captcha = MathCaptchaField()

    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['verifyemail'] = forms.EmailField(label="verify email", required=True, max_length=60)
        self.fields['year']=forms.ModelChoiceField(queryset=Year.objects.all(), widget=forms.HiddenInput())
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        'last_name','email','comment',Field('captcha', placeholder=" Enter Result"),
                        style="font-size: 25px; font-weight: bold;"
                        ,css_class="span6"
                    ),
                    Div(
                        'first_name','verifyemail',
                        style="font-size: 25px; font-weight: bold;"
                        ,css_class="span6"
                    ), css_class="span10"),
                css_class='row-fluid'),
        )
    class Meta:
        model = PhotoContestParticipant
        exclude = ("user", "validated")

    def clean_verifyemail(self):
        try:
            email = self.cleaned_data['email']
            verifyemail = self.cleaned_data['verifyemail']

            if email != verifyemail:
                raise forms.ValidationError("Emails do not match")
            return verifyemail
        except:
            raise forms.ValidationError("Emails do not match")