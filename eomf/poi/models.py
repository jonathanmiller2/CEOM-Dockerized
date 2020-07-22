import os, sys
from django.contrib.gis.db import models
import datetime
from django.contrib.auth.models import User
from eomf.photos.models import Category, Photo
from django.contrib.auth.models import User

class PixelDataset(models.Model):
    pixel_resolution = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=100,blank=False, null=False)
    ncol= models.IntegerField(null=False, blank=False)
    nrow = models.IntegerField(null=False, blank=False)
    def __unicode__(self):
        return self.name
    
class Pixel(models.Model):
    h = models.IntegerField(null=False, blank=False)
    v = models.IntegerField(null=False, blank=False)
    col = models.IntegerField(null=False, blank=False)
    row = models.IntegerField(null=False, blank=False)
    dataset = models.ForeignKey(PixelDataset, null=False, blank=False)
    
    class Meta:
        unique_together = (('h', 'v','col','row','dataset'),)
    def __unicode__(self):
        return u'%s: h%02dv%02d c:%s r:%s' % (self.dataset ,self.h,self.v,self.col,self.row) 
        

class PixelValidation(models.Model):
    pixel = models.ForeignKey(Pixel, null=False, blank=False)
    user = models.ForeignKey(User, null=False, blank=False)
    date_done = models.DateField(auto_now=True, auto_now_add=False)
    date_of_map = models.DateField(auto_now=True, auto_now_add=False)
    notes = models.TextField(blank=True)
    photo_used = models.ForeignKey(Photo, null=True, blank=True)
   
    def __unicode__(self):
        return u'%s -- %s' % (self.pixel,self.user) 

class PixelValidationLandcover(models.Model):
    validation = models.ForeignKey(PixelValidation, null=False, blank=False)
    category = models.ForeignKey(Category, null=False,blank=False)
    percentage = models.IntegerField(null=False, blank=False)

    class Meta:
        unique_together = (('validation','category'),)
    def __unicode__(self):
        return u'%s: %s %s %s category' % (self.validation,self.percentage,'%',self.category)

class Research(models.Model):
    name = models.CharField(max_length=100,blank=False, null=False, unique=True)
    description = models.TextField(blank=False, null=False)
    user = models.ForeignKey(User, null=False, blank=False)
    created = models.DateField(auto_now=False, auto_now_add=True)
    modified =  models.DateField(auto_now=True, auto_now_add=True)
    order = models.IntegerField(null=True, blank = True)
    def __unicode__(self):
        return u'%s' % (self.name)
class ResearchPixel(models.Model):
    pixel = models.ForeignKey(Pixel, null=False, blank=False)
    research = models.ForeignKey(Research, null=False, blank=False)
    user = models.ForeignKey(User, null=False, blank=False)
    private_id = models.CharField(max_length=30, null=True, blank = True)
    created = models.DateField(auto_now=False, auto_now_add=True)
    modified =  models.DateField(auto_now=True, auto_now_add=True)
    lat = models.FloatField(null=False, blank=False)
    lon = models.FloatField(null=False, blank=False)
    class Meta:
        unique_together = (('pixel','research'),)
    def __unicode__(self):
        return u'%s: %s (%s) ' % (self.research,self.pixel,self.user)
