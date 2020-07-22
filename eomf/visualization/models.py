from django.db import models
from django import forms
from eomf.inventory.models import Dataset
from django.core.exceptions import ValidationError

from eomf.photos.models import Category, Photo
from django.contrib.auth.models import User

import time
import csv

import json

def get_series_path(instance, filename):
    return time.strftime('timeseries/input')+filename

def get_seriesresult_path(instance, filename):
    return time.strftime('timeseries/%a%d%b%Y_%H-%M-%S_result_')+filename

MAX_BLANK_ROWS=100
MAX_SITES_PER_FILE=100
def checkFormat(document):
    try:
        dialect = csv.Sniffer().sniff(document.read(1024))
        document.seek(0, 0)
    except csv.Error:
        raise ValidationError(u'Not a valid CSV file')
    reader = csv.reader(document.read().splitlines(), dialect)
    i=1
    blank_rows=0
    for y_index, row in enumerate(reader):
        if i>MAX_SITES_PER_FILE:
            raise forms.ValidationError("The limit of sites per request is "+ str(MAX_SITES_PER_FILE)+". Please split the file in smaller chunks.")
        # ignore blank rows
        if not ''.join(str(x) for x in row):
            blank_rows+=1
            if blank_rows>= MAX_BLANK_ROWS:
                raise ValidationError(u'Too many blank rows in file. Please delete them')
            continue
        if len(row)!= 3:
            raise forms.ValidationError("Format error at line "+ str(i)+": More than three columns detected. ["+str(row)+"]")
        try:
            a = float(row[1])
            a = float(row[2])
        except Exception:
            raise forms.ValidationError("Format error at line "+ str(i)+": latitude and longitude must be in number format eg: 12.1234. ["+str(row)+"]")
        i+=1
    return True

#   This model holds all single site timeseries so that they can be accessed from the user panel later

class SingleTimeSeriesJob(models.Model):

    # task_id: unique id from celery updated upon task start
    task_id = models.CharField(null=True,blank=True,max_length=50)
    lon = models.FloatField(blank=False, null=False)
    lat = models.FloatField(blank=False, null=False)
    row = models.IntegerField(blank=True, null=True)
    col = models.IntegerField(blank=True, null=True)
    tile = models.CharField(max_length=6,blank=True, null=True)
    
    result = models.FileField(upload_to='visualization/timeseries/single', blank=True,null=True,max_length=300)
    years = models.CommaSeparatedIntegerField(max_length=150,verbose_name="Select years")
    product = models.ForeignKey(Dataset)

    # Information for current job state
    completed = models.BooleanField(default=False)
    user =  models.ForeignKey(User, null=False, blank=False, default=1096)

    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)
    
    def __unicode__(self):
        return str(self.user)+' ['+str(self.created)+']'

class TimeSeriesJob(models.Model):
    sender = models.EmailField(max_length=150,verbose_name='Additional sender',null=True,blank=True)
    points = models.FileField(upload_to='visualization/timeseries/input',max_length=150,validators=[checkFormat], verbose_name="Upload csv file")
    result = models.FileField(upload_to='visualization/timeseries/multi', blank=True,null=True,max_length=300)
    years = models.CommaSeparatedIntegerField(max_length=200,verbose_name="Select years")
    product = models.ForeignKey(Dataset)
    completed = models.BooleanField(default=False)
    working = models.BooleanField(default=False)
    error = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    user =  models.ForeignKey(User, null=False, blank=False, default=1096)

    message = models.CharField(max_length=150,blank=True,null=True)
    task_id = models.CharField(null=True,blank=True,max_length=50)
    total_sites = models.IntegerField(default=1)
    progress = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.sender
    def calculate_progress_percentage(self):
        if self.total_sites==0:
            return 0
        return int((self.progress*100)/self.total_sites)
    def toJSON(self):
        exclude_list = ['product','years','user','timestamp','']
        return json.dumps(dict([(attr, str(getattr(self, attr))) for attr in [f.name for f in self._meta.fields if f.name not in exclude_list]]))
