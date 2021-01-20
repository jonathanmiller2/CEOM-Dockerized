from django.forms import ModelForm
from django.db import models
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Layout, Field, Row, Div, Column, Fieldset
from crispy_forms.bootstrap import PrependedText
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.core.mail import send_mail

#capchta
from captcha.fields import CaptchaField
#from simplemathcaptcha.fields import MathCaptchaField

from eomf.outreach.models import Booth, Visitor, PhotoContestParticipant, Poster, Year, Survey, DemographicSurvey
from eomf.outreach.models import Workshop,WorkshopRegistration

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

class PosterForm(ModelForm):
    captcha = CaptchaField()
    #captcha = MathCaptchaField()
    def __init__(self, *args, **kwargs):
        super(PosterForm, self).__init__(*args, **kwargs)
        self.fields['verifyemail'] = forms.EmailField(label="verify email",required=True, max_length=60)
        self.fields['year']=forms.ModelChoiceField(queryset=Year.objects.all(), widget=forms.HiddenInput())
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'

        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Div('year',
                Div('form_errors',style="font-size: 25px; font-weight: bold;",css_class="span12"),
                Div(Div('last_name',style="font-size: 25px; font-weight: bold;",css_class="span6"), Div('first_name',style="font-size: 25px; font-weight: bold;",css_class="span6"),css_class='span12'),
                Div(Div('institution',style="font-size: 25px; font-weight: bold;",css_class="span6"), Div('department',style="font-size: 25px; font-weight: bold;",css_class="span6"),css_class='span12'),
                Div(Div('email',style="font-size: 25px; font-weight: bold;",css_class="span6"), Div('verifyemail',style="font-size: 25px; font-weight: bold;",css_class="span6"),css_class='span12'),
                Div(Div('title',style="font-size: 25px; font-weight: bold;",css_class='span6'),Div('category',style="font-size: 25px; font-weight: bold;",css_class='span6'),css_class='span12'),
                Div(Div('abstract',style="font-size: 25px; font-weight: bold;",css_class="span6"), Div('authors',style="font-size: 25px; font-weight: bold;",css_class="span6"),css_class='span12'),
                
                Div(Div('comment',style="font-size: 25px; font-weight: bold;",css_class='span6'), Div('preview',style="font-size: 25px; font-weight: bold;",css_class="span6"),css_class="span12"),
           css_class="span12"),
                Div( Div(Field('captcha', placeholder=" Enter Result"),style="font-size: 25px; font-weight: bold;",css_class="span6"), css_class='span12'),
        )

    class Meta:
        model = Poster
        exclude = ("created", "modified","validated")

    def clean_verifyemail(self):
        email = self.cleaned_data['email']
        verifyemail = self.cleaned_data['verifyemail']
        if email != verifyemail:
            raise forms.ValidationError("Emails do not match")
        return verifyemail

# class SurveyForm(ModelForm):
#     captcha = CaptchaField('Please enter the characters in the image')
#     def __init__(self, *args, **kwargs):
#         super(SurveyForm, self).__init__(*args, **kwargs)
#         self.fields['year']=forms.ModelChoiceField(queryset=Year.objects.all(), widget=forms.HiddenInput())
#         self.helper = FormHelper()
#         self.helper.form_class = 'form-horizontal'
#         self.helper.label_class = 'span2'
#         self.helper.field_class = 'span8'
#         self.helper.add_input(Submit('submit', 'Submit'))
#         self.helper.layout = Layout(
#             'year',
#             'participate_again',
#             'role',
#             'other_role',
#             'beneficial_aspects',
#             'comments_and_suggestions',
#             'captcha',
#         )
#     class Meta:
#         model = Survey
#         exclude = ("created","modified")
        
#     def clean_other_role(self):
#         other_role = self.cleaned_data["other_role"]
#         role = self.cleaned_data["role"]
#         if role!="Other" and (other_role != ""):
#             raise forms.ValidationError("Please select 'other' under role")
#         elif role=="Other" and other_role=="":
#             raise forms.ValidationError("Other role must be written")
#         return other_role

class DemographicSurveyForm(ModelForm):
    captcha = CaptchaField()
    def __init__(self, *args, **kwargs):
        super(DemographicSurveyForm, self).__init__(*args, **kwargs)
        self.fields['year']=forms.ModelChoiceField(queryset=Year.objects.all(), widget=forms.HiddenInput())
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'span2'
        self.helper.field_class = 'span8'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
                Div(Div('institution',css_class="span5"),Div('other_institution',css_class="span5"),css_class="span12"),
                Div(Div('position',css_class="span5"),Div('other_position',css_class="span5"),css_class="span12"),
                'highest_degree',
                'year',
                'gender',
                'ethnicity',
                'citizenship',
                Div(Div('race',css_class="span5"),Div('other_race',css_class="span5"),css_class="span12"),
                Div(Div('disability',css_class="span5"),Div('other_disability',css_class="span5"),css_class="span12"),
                'parents_degree',
                'captcha'
          
        )

    class Meta:
        model = DemographicSurvey
        exclude = ("created","modified")
        
    def clean_other_position(self):
            other_position = self.cleaned_data["other_position"]
            try:
                position = self.cleaned_data["position"]
            except:
                return other_position
            if position!="Other" and (other_position != ""):
                raise forms.ValidationError("Please select 'other' under position")
            elif position=="Other" and other_position=="":
                raise forms.ValidationError("Other position must be filled")
            return other_position

    def clean_other_institution(self):
            other_institution = self.cleaned_data["other_institution"]
            try:
                institution = self.cleaned_data["institution"]
            except:
                return other_institution
            if institution!="Other" and (other_institution != ""):
                raise forms.ValidationError("Please select 'other' under institution")
            elif institution=="Other" and other_institution=="":
                raise forms.ValidationError("Other institution must be filled")
            return other_institution
    def clean_other_race(self):
            other_race = self.cleaned_data["other_race"]
            try:
                race = self.cleaned_data["race"]
            except:
                return other_race
            if race!="Other" and (other_race != ""):
                raise forms.ValidationError("Please select 'other' under race")
            elif race=="Other" and other_race=="":
                raise forms.ValidationError("Other race must be filled")
            return other_race
    def clean_other_disability(self):
            other_disability = self.cleaned_data["other_disability"]
            try:
                disability = self.cleaned_data["disability"]
            except:
                return other_disability
            if disability!="Other" and (other_disability != ""):
                raise forms.ValidationError("Please select 'other' under disability")
            elif disability=="Other" and other_disability=="":
                raise forms.ValidationError("Other disability must be filled")
            return other_disability

class SurveyForm(ModelForm):
    captcha = CaptchaField()
    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        self.fields['year']=forms.ModelChoiceField(queryset=Year.objects.all(), widget=forms.HiddenInput())
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'span2'
        self.helper.field_class = 'span8'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
                HTML('<h3>Demographics</h3>'),
                Div(Div('institution',css_class="span5"),Div('other_institution',css_class="span5"),css_class="span12"),
                Div(Div('position',css_class="span5"),Div('other_position',css_class="span5"),css_class="span12"),
                'highest_degree',
                'year',
                'gender',
                'ethnicity',
                'citizenship',
                Div(Div('race',css_class="span5"),Div('other_race',css_class="span5"),css_class="span12"),
                Div(Div('disability',css_class="span5"),Div('other_disability',css_class="span5"),css_class="span12"),
                'parents_degree',
                HTML('<h3>Survey</h3>'),
                'participate_again',
                Div(Div('role',css_class="span5"),Div('other_role',css_class="span5"),css_class="span12"),
                'beneficial_aspects',
                'comments_and_suggestions',
                'captcha',
        )
          

    class Meta:
        model = Survey
        exclude = ("created","modified")
        
    def clean_other_position(self):
            other_position = self.cleaned_data["other_position"]
            try:
                position = self.cleaned_data["position"]
            except:
                return other_position
            if position!="Other" and (other_position != ""):
                raise forms.ValidationError("Please select 'other' under position")
            elif position=="Other" and other_position=="":
                raise forms.ValidationError("Other position must be filled")
            return other_position

    def clean_other_institution(self):
            other_institution = self.cleaned_data["other_institution"]
            try:
                institution = self.cleaned_data["institution"]
            except:
                return other_institution
            if institution!="Other" and (other_institution != ""):
                raise forms.ValidationError("Please select 'other' under institution")
            elif institution=="Other" and other_institution=="":
                raise forms.ValidationError("Other institution must be filled")
            return other_institution
    def clean_other_race(self):
            other_race = self.cleaned_data["other_race"]
            try:
                race = self.cleaned_data["race"]
            except:
                return other_race
            if race!="Other" and (other_race != ""):
                raise forms.ValidationError("Please select 'other' under race")
            elif race=="Other" and other_race=="":
                raise forms.ValidationError("Other race must be filled")
            return other_race
    def clean_other_disability(self):
            other_disability = self.cleaned_data["other_disability"]
            try:
                disability = self.cleaned_data["disability"]
            except:
                return other_disability
            if disability!="Other" and (other_disability != ""):
                raise forms.ValidationError("Please select 'other' under disability")
            elif disability=="Other" and other_disability=="":
                raise forms.ValidationError("Other disability must be filled")
            return other_disability    
    def clean_other_role(self):
        other_role = self.cleaned_data["other_role"]
        try:
            role = self.cleaned_data["role"]
        except:
            return other_role
        if role!="Other" and (other_role != ""):
            raise forms.ValidationError("Please select 'other' under role")
        elif role=="Other" and other_role=="":
            raise forms.ValidationError("Other role must be written")
        return other_role

class volunteerForm(forms.Form):
    roles = (
        (1,'UnderGraduate'),
        (2,'Graduate'),
        (3,'Post Doc'),
        (4,'Poster Judge'),
        (5,'Committee Member'),
        )
    lunch_choice = (
        (1,'Yes'),
        (2,'No'),
        )
    tshirt_choices = (
        (1,'Small'),
        (2,'Medium'),
        (3,'Large'),
        (4,'XL'),
        (5,'XXL'),
        )
    Last_Name = forms.CharField(max_length=128)
    First_Name = forms.CharField(max_length=128)
    Primary_Role = forms.ChoiceField(choices=roles)
    Lunch = forms.ChoiceField(choices=lunch_choice)
    TShirt_size = forms.ChoiceField(choices=tshirt_choices)
    #class Meta:
    #    model = TestModel
    #    fields = ('name','attendingAs','tshirtSize','lunch')



class WorkshopRegistrationForm(ModelForm):
    captcha = CaptchaField()

    #TODO: Remove all this debug shit last guy left behind

    def __init__(self, *args, **kwargs):
        try:
            self.workshop = kwargs.pop('data')
        except AttributeError:
            try:
                self.workshop = kwargs.pop('request')
            except:
                print("i dont know what happened")
            print("i got a Attribute error probably because you sent me a post request and i dont know how to handle")
        except KeyError:
            print("i dont know what hit me!")
            try:
                self.workshop = kwargs.pop('request')
            except:
                print("i dont know what happened")
            print("i got a Attribute error probably because you sent me a post request and i dont know how to handle")
        print("i came here:")
        #print self.workshop
        #send_mail('debug:worshop forms', str(type(self))+":"+str(kwargs)+" args: "+str(args), 'admin@eomf.ou.edu', ['bhargavreddy.bolla@ou.edu','bhargavreddy.bolla@gmail.com'], fail_silently=True)
        # foo = open("/media/foo.txt",'a')
        # foo.write(str(kwargs)+" args: "+str(args))
        # foo.close()
        #print self
        super(WorkshopRegistrationForm, self).__init__(*args, **kwargs)
        #send_mail('debug:worshop forms2', str(type(self))+str(args[0][unicode('workshop')])+":"+str(kwargs)+" args: "+str(args), 'admin@eomf.ou.edu', ['bhargavreddy.bolla@ou.edu','bhargavreddy.bolla@gmail.com'], fail_silently=True)
        try:    
            self.fields['workshop']=forms.ModelChoiceField(queryset=Workshop.objects.all(), widget=forms.HiddenInput(),initial=self.workshop.id)
            self.fields['verifyemail'] = forms.EmailField(label="verify email",required=True, max_length=60)
            # Extra fields:
            for i in range(1,4):
                self.fields['extra_boolean_field'+str(i)] = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput())
                self.fields['extra_text_field'+str(i)] = forms.CharField(required=False,max_length=100,widget=forms.HiddenInput())

            if self.workshop.extra_boolean_field1 is not None and self.workshop.extra_boolean_field1 != '':
                self.fields['extra_boolean_field1'] = forms.BooleanField(required=False,initial=False,label=self.workshop.extra_boolean_field1)
            if self.workshop.extra_boolean_field2 is not None and self.workshop.extra_boolean_field2 != '':
                self.fields['extra_boolean_field2'] = forms.BooleanField(required=False,initial=False,label=self.workshop.extra_boolean_field2)
            if self.workshop.extra_boolean_field3 is not None and self.workshop.extra_boolean_field3 != '':
                self.fields['extra_boolean_field3'] = forms.BooleanField(required=False,initial=False,label=self.workshop.extra_boolean_field3)
            
            if self.workshop.extra_text_field1 is not None and self.workshop.extra_text_field1 != '':
                self.fields['extra_text_field1'] = forms.CharField(required=False,max_length=100,label=self.workshop.extra_text_field1,widget=forms.TextInput(attrs={'size':'100'}))
            if self.workshop.extra_text_field2 is not None and self.workshop.extra_text_field2 != '':
                self.fields['extra_text_field2'] = forms.CharField(required=False,max_length=100,label=self.workshop.extra_text_field2,widget=forms.TextInput(attrs={'size':'100'}))
            if self.workshop.extra_text_field3 is not None and self.workshop.extra_text_field3 != '':
                self.fields['extra_text_field3'] = forms.CharField(required=False,max_length=100,label=self.workshop.extra_text_field3,widget=forms.TextInput(attrs={'size':'100'}))

            self.helper = FormHelper()
            self.helper.form_class = 'form-horizontal'
            self.helper.layout = Layout(
                Div('workshop',
                    Div('form_errors',style="font-size: 25px;  font-weight: bold;",css_class="span12"),
                    Div(Div('first_name',style="font-size: 25px;  font-weight: bold;",css_class="span5"), Div('last_name',style="font-size: 25px;  font-weight: bold;",css_class="span5 offset1"),css_class='span12'),
                    Div(Div('institution',style="font-size: 25px;  font-weight: bold;",css_class="span5"), Div('position',style="font-size: 25px;  font-weight: bold;",css_class="span5 offset1"),css_class='span12'),
                    Div(Div('address',style="font-size: 25px;  font-weight: bold;",css_class="span5"), Div('area_of_expertise',style="font-size: 25px;  font-weight: bold;",css_class="span5 offset1"),css_class='span12'),
                    Div(Div('email',style="font-size: 25px;  font-weight: bold;",css_class="span5"), Div('verifyemail',style="font-size: 25px;  font-weight: bold;",css_class="span5 offset1"),css_class='span12'),
                    Div(Div('phone',style="font-size: 25px;  font-weight: bold;",css_class="span5"), Div('international_phone',style="font-size: 25px;  font-weight: bold;",css_class="span5 offset1"),css_class='span12'),
                    Div(Div('extra_boolean_field1',style="font-size: 25px;  font-weight: bold;",css_class="span5"), Div('extra_boolean_field2',style="font-size: 25px;  font-weight: bold;",css_class="span5"),css_class='span12'),
                    Div(Div('extra_boolean_field3',style="font-size: 25px;  font-weight: bold;",css_class="span6"), Div('extra_text_field1',style="font-size: 25px; margin-left: 50px; font-weight: bold;",css_class="span5"),css_class='span12'),
                    Div(Div('extra_text_field2',style="font-size: 25px;  font-weight: bold;",css_class="span6"), Div('extra_text_field3',style="font-size: 25px;  font-weight: bold;",css_class="span5"),css_class='span12'),
                    Div(Div(Field('captcha', placeholder=" Enter Result"),style="font-size: 25px;  font-weight: bold;",css_class="span12"),css_class='span12'),
                    # PrependedText('captcha', '=', placeholder="Enter Result")
                )
            )
            
            self.helper.add_input(Submit('submit', 'Submit'))
        except:
            pass

    class Meta:
        model = WorkshopRegistration
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

class WorkshopRegistrationWithPassword(WorkshopRegistrationForm):
    password = forms.CharField(label="Password",help_text='This is a closed workshop and requires a password to register.',required=True, max_length=20,widget=forms.PasswordInput(render_value = True))
    def __init__(self, *args, **kwargs):
        super(WorkshopRegistrationWithPassword, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Div('workshop',
                Div('password',style="font-size: 25px;  font-weight: bold;",css_class="span12"),
                Div('form_errors',style="font-size: 25px;  font-weight: bold;",css_class="span12"),
                Div(Div('first_name',style="font-size: 25px;  font-weight: bold;",css_class="span5"), Div('last_name',style="font-size: 25px;  font-weight: bold;",css_class="span5 offset1"),css_class='span12'),
                Div(Div('institution',style="font-size: 25px;  font-weight: bold;",css_class="span5"), Div('position',style="font-size: 25px;  font-weight: bold;",css_class="span5 offset1"),css_class='span12'),
                Div(Div('address',style="font-size: 25px;  font-weight: bold;",css_class="span5"), Div('area_of_expertise',style="font-size: 25px;  font-weight: bold;",css_class="span5 offset1"),css_class='span12'),
                Div(Div('email',style="font-size: 25px;  font-weight: bold;",css_class="span5"), Div('verifyemail',style="font-size: 25px;  font-weight: bold;",css_class="span5 offset1"),css_class='span12'),
                Div(Div('phone',style="font-size: 25px;  font-weight: bold;",css_class="span5"), Div('international_phone',style="font-size: 25px;  font-weight: bold;",css_class="span5 offset1"),css_class='span12'),
                Div(Div('extra_boolean_field1',style="font-size: 25px;  font-weight: bold;",css_class="span5"), Div('extra_boolean_field2',style="font-size: 25px;  font-weight: bold;",css_class="span5 offset1"),css_class='span12'),
                'extra_boolean_field3',
                Div(Div('extra_text_field1',style="font-size: 25px;  font-weight: bold;",css_class="span5"), Div('extra_text_field2',style="font-size: 25px;  font-weight: bold;",css_class="span5 offset1"),css_class='span12'),
                'extra_text_field3',    
                Div(Div('captcha',style="font-size: 25px;  font-weight: bold;",css_class="span12"),css_class='span12'),
            )
        )
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_password(self):
        if self.cleaned_data['password'] == self.workshop.password:
            return self.cleaned_data['password']
        else:
            raise forms.ValidationError('Password is not correct.')