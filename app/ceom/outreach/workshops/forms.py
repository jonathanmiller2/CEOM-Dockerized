from django.forms import ModelForm
from django.db import models
from django import forms
from ceom.outreach.workshops.models import Workshop,WorkshopRegistration
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Layout, Field, Row, Div, Column
from crispy_forms.bootstrap import PrependedText
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.core.mail import send_mail

#capchta
from captcha.fields import CaptchaField

# class WorkshopRegistrationForm(ModelForm):
#     captcha = CaptchaField()

#     def __init__(self, *args, **kwargs):
#         print("what is in kwargs: ")
#         print (kwargs)
#         try:
#             self.workshop = kwargs.pop('data')
#         except AttributeError:
#             try:
#                 self.workshop = kwargs.pop('request')
#             except:
#                 pass
                
#         except KeyError:
#             try:
#                 self.workshop = kwargs.pop('request')
#             except:
#                 pass
       
#         super(WorkshopRegistrationForm, self).__init__(*args, **kwargs)
      
#         try:    
#             self.fields['workshop']=forms.ModelChoiceField(queryset=Workshop.objects.all(), widget=forms.HiddenInput(),initial=self.workshop.id)
#             self.fields['verifyemail'] = forms.EmailField(label="verify email",required=True, max_length=60)
#             # Extra fields:
#             for i in range(1,4):
#                 self.fields['extra_boolean_field'+str(i)] = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput())
#                 self.fields['extra_text_field'+str(i)] = forms.CharField(required=False,max_length=100,widget=forms.HiddenInput())

#             if self.workshop.extra_boolean_field1 is not None and self.workshop.extra_boolean_field1 != '':
#                 self.fields['extra_boolean_field1'] = forms.BooleanField(required=False,initial=False,label=self.workshop.extra_boolean_field1)
#             if self.workshop.extra_boolean_field2 is not None and self.workshop.extra_boolean_field2 != '':
#                 self.fields['extra_boolean_field2'] = forms.BooleanField(required=False,initial=False,label=self.workshop.extra_boolean_field2)
#             if self.workshop.extra_boolean_field3 is not None and self.workshop.extra_boolean_field3 != '':
#                 self.fields['extra_boolean_field3'] = forms.BooleanField(required=False,initial=False,label=self.workshop.extra_boolean_field3)
            
#             if self.workshop.extra_text_field1 is not None and self.workshop.extra_text_field1 != '':
#                 self.fields['extra_text_field1'] = forms.CharField(required=False,max_length=100,label=self.workshop.extra_text_field1,widget=forms.TextInput(attrs={'size':'100'}))
#             if self.workshop.extra_text_field2 is not None and self.workshop.extra_text_field2 != '':
#                 self.fields['extra_text_field2'] = forms.CharField(required=False,max_length=100,label=self.workshop.extra_text_field2,widget=forms.TextInput(attrs={'size':'100'}))
#             if self.workshop.extra_text_field3 is not None and self.workshop.extra_text_field3 != '':
#                 self.fields['extra_text_field3'] = forms.CharField(required=False,max_length=100,label=self.workshop.extra_text_field3,widget=forms.TextInput(attrs={'size':'100'}))

#             self.helper = FormHelper()
#             self.helper.form_class = 'form-horizontal'
#             self.helper.layout = Layout(
#                 Div('workshop',
#                     Div(Div('first_name',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), Div('last_name',style="font-size: 25px;  font-weight: bold;",css_class="col-6-offset-2"),css_class='row'),
#                     Div(Div('institution',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), Div('position',style="font-size: 25px;  font-weight: bold;",css_class="col-6"),css_class='row'),
#                     Div(Div('address',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), Div('area_of_expertise',style="font-size: 25px;  font-weight: bold;",css_class="col-6 offset1"),css_class='row'),
#                     Div(Div('email',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), Div('verifyemail',style="font-size: 25px;  font-weight: bold;",css_class="col-6 offset1"),css_class='row'),
#                     Div(Div('phone',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), css_class='row'),
#                     Div(Div('extra_boolean_field1',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), Div('extra_boolean_field2',style="font-size: 25px;  font-weight: bold;",css_class="col-6"),css_class='row'),
#                     Div(Div('extra_boolean_field3',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), Div('extra_text_field1',style="font-size: 25px; margin-left: 50px; font-weight: bold;",css_class="col-6"),css_class='row'),
#                     Div(Field('extra_text_field2',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), Div('extra_text_field3',style="font-size: 25px;  font-weight: bold;",css_class="col-6"),css_class='row'),
#                     Div(Div(Field('captcha', placeholder=" Enter Result"),style="font-size: 25px;  font-weight: bold;",css_class="col-6"),css_class='row'),
#                     # PrependedText('captcha', '=', placeholder="Enter Result")
#                 )
#             )
            
#             self.helper.add_input(Submit('submit', 'Submit'))
#         except:
#             pass

#     class Meta:
#         model = WorkshopRegistration
#         exclude = ("created", "modified", "validated")

#     def clean_verifyemail(self):
#         try:
#             email = self.cleaned_data['email']
#         except:
#             raise forms.ValidationError("Above email in wrong format")
#         verifyemail = self.cleaned_data['verifyemail']
#         if email != verifyemail:
#             raise forms.ValidationError("Emails do not match")
#         return verifyemail

# class WorkshopRegistrationWithPassword(WorkshopRegistrationForm):
#     password = forms.CharField(label="Password",help_text='This is a closed workshop and requires a password to register.',required=True, max_length=20,widget=forms.PasswordInput(render_value = True))
#     def __init__(self, *args, **kwargs):
#         super(WorkshopRegistrationWithPassword, self).__init__(*args, **kwargs)
#         self.helper.layout = Layout(
#             Div('workshop',
#                 Div('password',style="font-size: 25px;  font-weight: bold;",css_class="row"),
#                 Div(Div('first_name',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), Div('last_name',style="font-size: 25px;  font-weight: bold;",css_class="col-6-offset-2"),css_class='row'),
#                 Div(Div('institution',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), Div('position',style="font-size: 25px;  font-weight: bold;",css_class="col-6 offset1"),css_class='row'),
#                 Div(Div('address',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), Div('area_of_expertise',style="font-size: 25px;  font-weight: bold;",css_class="col-6 offset1"),css_class='row'),
#                 Div(Div('email',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), Div('verifyemail',style="font-size: 25px;  font-weight: bold;",css_class="col-6 offset1"),css_class='row'),
#                 Div(Div('phone',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), css_class='row'),
#                 Div(Div('extra_boolean_field1',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), Div('extra_boolean_field2',style="font-size: 25px;  font-weight: bold;",css_class="col-6 offset1"),css_class='row'),
#                 'extra_boolean_field3',
#                 Div(Field('extra_text_field1',style="font-size: 25px;  font-weight: bold;",css_class="col-6"), Div('extra_text_field2',style="font-size: 25px;  font-weight: bold;",css_class="col-6 offset1"),css_class='row'),
#                 'extra_text_field3',    
#                 Div(Div('captcha',style="font-size: 25px;  font-weight: bold;",css_class="col-6"),css_class='row'),
#             )
#         )
#         self.helper.add_input(Submit('submit', 'Submit'))

    # def clean_password(self):
    #     if self.cleaned_data['password'] == self.workshop.password:
    #         return self.cleaned_data['password']
    #     else:
    #         raise forms.ValidationError('Password is not correct.')