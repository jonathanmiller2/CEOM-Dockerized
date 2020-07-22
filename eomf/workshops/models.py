from django.db import models
from django.contrib.gis.db import models
from tinymce import models as tinymce_models
from localflavor.us.models import PhoneNumberField as USPhone
from phonenumber_field.modelfields import PhoneNumberField as InternationalPhone
from django.contrib.auth.models import User
# Create your models here.

class Workshop(models.Model):
    name = models.CharField(max_length=500,null=False,blank=False)
    category = models.ForeignKey('WorkshopClass')
    date_start = models.DateField(null=False,blank=False)
    date_end = models.DateField(null=False,blank=False)
    password = models.CharField(max_length=20,null=True, blank=True,help_text="Enter a password if the user needs a password to register (eg: Closed workshops)")
    content = tinymce_models.HTMLField(null=True,blank=True)
    address = models.CharField(max_length=300,blank=True,null=True)
    city = models.CharField(max_length=300,blank=True,null=True)
    country = models.CharField(max_length=300,blank=True,null=True)
    registration_open = models.BooleanField(default=False, null=False)
    description = models.TextField(null=True)
    admin_emails = models.CharField(max_length=1000,null=False,blank=False, default = 'gisday@ou.edu')
    registration_message = tinymce_models.HTMLField(null=True,blank=True)
    agenda = models.FileField(null=True, max_length=300,upload_to="workshops/agendas/", blank=True)

    extra_boolean_field1 = models.CharField(max_length=100, null=True, blank=True)
    extra_boolean_field2 = models.CharField(max_length=100, null=True, blank=True)
    extra_boolean_field3 = models.CharField(max_length=100, null=True, blank=True)

    extra_text_field1 = models.CharField(max_length=100, null=True, blank=True)
    extra_text_field2 = models.CharField(max_length=100, null=True, blank=True)
    extra_text_field3 = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u'%s (%d)' % (self.name, self.date_start.year)
    class Meta:
        unique_together = (('name',),)

class SponsorInWorkshop(models.Model):
    workshop = models.ForeignKey('Workshop')
    sponsor = models.ForeignKey('Sponsor')
    def __unicode__(self):
        return u'%s' % (self.sponsor)
    class Meta:
        unique_together = (('workshop','sponsor'),)
class Sponsor(models.Model):
    name = models.CharField(max_length=200,null=False,blank=False)
    logo = models.FileField(null=False, max_length=300,upload_to="workshops/sponsors/")
    def __unicode__(self):
        return u'%s' % (self.name)
    class Meta:
        unique_together = (('name',),)
class WorkshopClass(models.Model):
    name = models.CharField(max_length=200,null=False,blank=False)
    image = models.ImageField(upload_to="workshops/categories", null=False)
    class Meta:
        unique_together = (('name',),)
    def __unicode__(self):
        return u'%s' % (self.name)

class WorkshopRegistration(models.Model):
    workshop = models.ForeignKey(Workshop, related_name='workshop', related_query_name='workshop')
    first_name = models.CharField(max_length=100,null=False,blank=False)
    last_name = models.CharField(max_length=100,null=False,blank=False)
    position = models.CharField(max_length=300,null=False,blank=False)
    institution = models.CharField(max_length=200,null=False,blank=False)
    address = models.CharField(max_length=200,null=False,blank=False)
    email = models.EmailField(null=False,blank=False)
    phone = USPhone(null=False, blank = False)
    international_phone = InternationalPhone(null=True, blank = True)
    area_of_expertise = models.CharField(max_length=300,null=False,blank=False)
    # Migrated to exta_boolean_field1
    # requests_travel_assistance = models.BooleanField(null=False, default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    validated = models.BooleanField()


    extra_boolean_field1 = models.BooleanField(default=False)
    extra_boolean_field2 = models.BooleanField(default=False)
    extra_boolean_field3 = models.BooleanField(default=False)

    extra_text_field1 = models.CharField(max_length=100, null=True, blank=True)
    extra_text_field2 = models.CharField(max_length=100, null=True, blank=True)
    extra_text_field3 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = (('workshop','email'),)
    def __unicode__(self):
        return u'%s, %s (%s)' % (self.last_name,self.first_name,self.workshop)


class WorkshopPhoto(models.Model):

    workshop = models.ForeignKey('Workshop',related_name='workshop_images')
    image = models.FileField(upload_to="workshops/photos", null=True, blank=True)
    priority = models.PositiveIntegerField(default=99999)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = (('workshop','image'),)
    @property
    def filename(self):
        return self.image.name.rsplit('/', 1)[-1]
class Institution(models.Model):
    name = models.CharField(max_length=200,null=False,blank=False)
    link = models.CharField(max_length=300,null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = (('name',),)
    def __unicode__(self):
        return u'%s' % (self.name)


class Presentation(models.Model):
    workshop = models.ForeignKey(Workshop)
    title = models.CharField(max_length=200,null=False,blank=False)
    first_name = models.CharField(max_length=100,null=False,blank=False)
    last_name = models.CharField(max_length=100,null=False,blank=False)
    other_presenters = models.CharField(max_length=200,null=False,blank=True)
    content = models.FileField(null=True, max_length=300,upload_to="workshops/presentations/", blank=True)
    institution = models.ForeignKey(Institution)
    time_ini = models.DateTimeField(null=False)
    time_end = models.DateTimeField(null=True) 
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = (('workshop','time_ini'),)
    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.workshop)