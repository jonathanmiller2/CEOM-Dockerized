from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from ceom.photos.models import Category, Photo

import time, csv, json, datetime

class Dataset(models.Model):
    name = models.CharField(max_length=7, primary_key=True)
    xdim = models.FloatField()
    ydim = models.FloatField()
    grid_size = models.FloatField()
    projcode = models.IntegerField(null=True, blank=True)
    zonecode = models.IntegerField(null=True, blank=True)
    spherecode = models.IntegerField(null=True, blank=True)
    projparm = models.CharField(max_length=1000, null=True, blank=True)
    grid_name = models.CharField(max_length=100, null=True, blank=True)
    ordering = models.FloatField(null=True, blank=True)
    long_name = models.CharField(max_length=100, null=True, blank=True)
    short_name = models.CharField(max_length=5, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    day_res = models.IntegerField(default=8)
    is_global = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=10, primary_key=True)
    long_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class MODISSingleTimeSeriesJob(models.Model):
    # task_id: unique id from celery updated upon task start
    task_id = models.CharField(null=True,blank=True,max_length=50)
    h = models.IntegerField(blank=True, null=True)
    v = models.IntegerField(blank=True, null=True)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)
    result = models.FileField(upload_to='modis/timeseries/single', blank=True,null=True,max_length=300)
    years = ArrayField(models.CharField(max_length=4))
    working = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    errored = models.BooleanField(default=False)
    percent_complete = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(User, default=1096, on_delete=models.CASCADE)

    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)
    
    def __str__(self):
        return str(self.user)+' ['+str(self.created)+']'

class MODISMultipleTimeSeriesJob(models.Model):
    # task_id: unique id from celery updated upon task start
    task_id = models.CharField(null=True,blank=True,max_length=50)
    points = models.FileField(upload_to='modis/timeseries/multi/input/', max_length=150)
    result = models.FileField(upload_to='modis/timeseries/multi/output/', blank=True, null=True, max_length=300)
    years = ArrayField(models.CharField(max_length=4))
    working = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    errored = models.BooleanField(default=False)
    percent_complete = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(User, default=1096, on_delete=models.CASCADE)
    
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)
    
    def __str__(self):
        return str(self.user)+' ['+str(self.created)+']'