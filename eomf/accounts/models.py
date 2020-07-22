from django.contrib.gis.db import models
from django import forms
from django.contrib.auth.models import User
from fields import CountryField
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy  as _

class Profile(models.Model):
    user = models.OneToOneField(User, unique=True)
    country = CountryField(verbose_name=_("Country"),null=True,blank=True) 
    affiliation = models.CharField(verbose_name=_("Affiliation"),max_length=250, null=True, blank=True)
    telephone = models.CharField(verbose_name=_("Telephone"),max_length=20, null=True, blank=True)
    address1 = models.CharField(verbose_name=_("Address1"),max_length=50, null=True, blank=True)
    address2 = models.CharField(verbose_name=_("Address2"),max_length=50, null=True, blank=True)
    city = models.CharField(verbose_name=_("City"),max_length=50, null=True, blank=True)
    state = models.CharField(verbose_name=_("State"),max_length=80, null=True, blank=True)
    postal = models.CharField(verbose_name=_("Postal code"),max_length=10, null=True, blank=True)
    url = models.CharField(verbose_name=_("URL"),max_length=100, null=True, blank=True)
    gisday = models.NullBooleanField(verbose_name=_("Attending GIS Day"), blank=True, null=True)

    def get_all_fields(self):
        """Returns a list of all field names on the instance."""
        fields = []
        for f in self._meta.fields:

            fname = f.name        
            # resolve picklists/choices, with get_xyz_display() function
            get_choice = 'get_'+fname+'_display'
            if hasattr( self, get_choice):
                value = getattr( self, get_choice)()
            else:
                try :
                    value = getattr(self, fname)
                except User.DoesNotExist:
                    value = None

            # only display fields with values and skip some fields entirely
            if f.editable and value and f.name not in ('id', 'status', 'workshop', 'user', 'complete') :

                fields.append(
                  {
                   'label':f.verbose_name, 
                   'name':f.name, 
                   'value':value,
                  }
                )
        return fields
    
    def __unicode__(self):
        return self.user.username

def user_post_save(sender, instance, **kwargs):
    profile, new = Profile.objects.get_or_create(user=instance)

models.signals.post_save.connect(user_post_save, User)

