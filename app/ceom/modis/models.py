#This class describes the inventory data model in Django
# model syntax

from django.db import models
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_comma_separated_integer_list

from ceom.photos.models import Category, Photo
from django.contrib.auth.models import User

import time
import csv

import json

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
    # timeseries_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=10, primary_key=True)
    long_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Tile(models.Model):
    name = models.CharField(max_length=6, primary_key=True)
    upleftx = models.FloatField(null=True)
    uplefty = models.FloatField(null=True)
    lowrightx = models.FloatField(null=True)
    lowrighty = models.FloatField(null=True)
    iv = models.IntegerField()
    ih = models.IntegerField()
    lon_min = models.FloatField(null=True)
    lon_max = models.FloatField(null=True)
    lat_min = models.FloatField(null=True)
    lat_max = models.FloatField(null=True)
    continent = models.CharField(max_length=30,null=True)

    def toString(self):
        return self.name + ";ih=" + str(self.ih) + ";long_min=" \
               + str(self.lon_min) +";" + self.continent + ";"

    def __str__(self):
        return self.name
        
class File(models.Model):
    tile = models.ForeignKey(Tile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, primary_key=True)
    year = models.IntegerField(null=True)
    day = models.IntegerField(null=True)
    timestamp = models.BigIntegerField()
    dataset = models.ForeignKey(Dataset, null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='Process')
    absolute_path = models.CharField(max_length = 300, null=False, default='N/A')
    def __str__(self):
        return self.name

class Process(models.Model):
    file = models.ForeignKey(File, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField('date processed', null=True, blank=True)


def get_series_path(instance, filename):
    return time.strftime('timeseries/input')+filename

def get_seriesresult_path(instance, filename):
    return time.strftime('timeseries/%a%d%b%Y_%H-%M-%S_result_')+filename

MAX_BLANK_ROWS=100
MAX_SITES_PER_FILE=100
def checkFormat(document):
    try:
        dialect = csv.Sniffer().sniff(document.read(1024).decode('utf-8'))
        document.seek(0, 0)
    except csv.Error:
        raise ValidationError('fNot a valid CSV file')
    reader = csv.reader(document.read().decode('utf-8').splitlines(), dialect)
    i=1
    blank_rows=0
    for y_index, row in enumerate(reader):
        if i>MAX_SITES_PER_FILE:
            raise forms.ValidationError("The limit of sites per request is "+ str(MAX_SITES_PER_FILE)+". Please split the file in smaller chunks.")
        # ignore blank rows
        if not ''.join(str(x) for x in row):
            blank_rows+=1
            if blank_rows>= MAX_BLANK_ROWS:
                raise ValidationError('Too many blank rows in file. Please delete them')
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

class MODISSingleTimeSeriesJob(models.Model):

    # task_id: unique id from celery updated upon task start
    task_id = models.CharField(null=True,blank=True,max_length=50)
    lon = models.FloatField(blank=False, null=False)
    lat = models.FloatField(blank=False, null=False)
    row = models.IntegerField(blank=True, null=True)
    col = models.IntegerField(blank=True, null=True)
    tile = models.CharField(max_length=6,blank=True, null=True)
    
    result = models.FileField(upload_to='modis/timeseries/single', blank=True,null=True,max_length=300)
    years = models.CharField(validators=[validate_comma_separated_integer_list], max_length=150,verbose_name="Select years")
    product = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    # Information for current job state
    completed = models.BooleanField(default=False)
    user =  models.ForeignKey(User, null=False, blank=False, default=1096, on_delete=models.CASCADE)

    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)
    
    def __str__(self):
        return str(self.user)+' ['+str(self.created)+']'

class MODISMultipleTimeSeriesJob(models.Model):
    sender = models.EmailField(max_length=150,verbose_name='Additional sender',null=True,blank=True)
    points = models.FileField(upload_to='modis/timeseries/input',max_length=150,validators=[checkFormat], verbose_name="Upload csv file")
    result = models.FileField(upload_to='modis/timeseries/multi', blank=True,null=True,max_length=300)
    years = models.CharField(validators=[validate_comma_separated_integer_list], max_length=200,verbose_name="Select years")
    product = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    working = models.BooleanField(default=False)
    error = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    user =  models.ForeignKey(User, null=False, blank=False, default=1096, on_delete=models.CASCADE)

    message = models.CharField(max_length=150,blank=True,null=True)
    task_id = models.CharField(null=True,blank=True,max_length=50)
    total_sites = models.IntegerField(default=1)
    progress = models.IntegerField(default=0)

    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)
    
    def __str__(self):
        return self.sender
    def calculate_progress_percentage(self):
        if self.total_sites==0:
            return 0
        return int((self.progress*100)/self.total_sites)
    def toJSON(self):
        exclude_list = ['product','years','user','timestamp','']
        return json.dumps(dict([(attr, str(getattr(self, attr))) for attr in [f.name for f in self._meta.fields if f.name not in exclude_list]]))

