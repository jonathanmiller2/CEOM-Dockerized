from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from ceom.accounts.models import Profile
from django.contrib.gis import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import AuthenticationForm

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

#TODO: Remove all references to crispy forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div


class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('submit', 'Save'))
        
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'validate form-control form-control-sm','placeholder': 'Username'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder':'Password'}), label='')


class InitModelForm(forms.ModelForm):
    """
    Subclass of `forms.ModelForm` that makes sure the initial values
    are present in the form data, so you don't have to send all old values
    for the form to actually validate.
    """
    def merge_from_initial(self):
        filt = lambda v: v not in list(self.data.keys())
        for field in filter(filt, getattr(self.Meta, 'fields', ())):
            self.data[field] = self.initial.get(field, None)

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
#attrs_dict = {'class': 'required'}
#TODO: Is this^ needed ?

#class RegisterForm(UserCreationForm):
#
#    firstname = forms.CharField(max_length=100, help_text='First name')
#    lastname = forms.CharField(max_length=100, help_text='Last name')
#
#    class Meta:
#        model = Profile
#        fields = ["username", "password1", "password2", "firstname", "lastname", "country", "affiliation", "telephone", "address1", "address2", "city", "state", "postal", "url"]

#TODO: Adapt this registration form to inherit from Django's UserCreationForm? (as shown above)
class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.

    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    username = forms.RegexField(
        regex=r'^\w+$',
        max_length=30,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}),
        label=_("Username"),
        error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")}
    )

    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm'})
    )

    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm'})
    )

    email = forms.EmailField(
        max_length=75,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm'})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm'}, render_value=False),
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm'}, render_value=False),
    )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)



    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """

        if User.objects.filter(email__iexact=self.cleaned_data['email']).count():
            raise forms.ValidationError(_('This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

    def save(self, commit=True):
        u = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.is_active = True
        if commit:
            u.save()
        return u



class UserForm(InitModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(InitModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

    country = CountryField(blank=True,).formfield(
        required=False,
        widget=forms.Select(attrs={'class':'form-control form-control-sm'})
    )

    affiliation = forms.CharField(
        max_length=250,
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm'})
    )

    telephone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm'})
    )

    address1 = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm'})
    )

    address2 = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm'})
    )

    city = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm'})
    )

    state = forms.CharField(
        max_length=80,
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm'})
    )

    postal = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm'})
    )

    url = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm'})
    )

    class Meta:
        model = Profile
        fields = (
            'country',
            'affiliation',
            'address1',
            'address2',
            'telephone',
            'postal',
            'url'
        )
        exclude = ('user',)
