from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

import json



MAX_BLANK_ROWS=100
MAX_SITES_PER_FILE=100
def checkFormat(document):
    try:
        dialect = csv.Sniffer().sniff(document.read(1024).decode('utf-8'))
        document.seek(0, 0)
    except csv.Error:
        raise ValidationError('Not a valid CSV file')
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




class TROPOMISingleTimeSeriesJob(models.Model):
    # task_id: unique id from celery updated upon task start
    task_id = models.CharField(null=True,blank=True,max_length=50)
    pixelx = models.IntegerField(blank=True, null=True)
    pixely = models.IntegerField(blank=True, null=True)
    result = models.FileField(upload_to='tropomi/timeseries/single', blank=True,null=True,max_length=300)
    years = ArrayField(models.CharField(max_length=4))
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, default=1096, on_delete=models.CASCADE)

    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)
    
    def __str__(self):
        return str(self.user)+' ['+str(self.created)+']'

class TROPOMIMultipleTimeSeriesJob(models.Model):
    # task_id: unique id from celery updated upon task start
    task_id = models.CharField(null=True,blank=True,max_length=50)
    points = models.FileField(upload_to='tropomi/timeseries/input', max_length=150, validators=[checkFormat])
    result = models.FileField(upload_to='tropomi/timeseries/multi', blank=True, null=True, max_length=300)
    years = ArrayField(models.CharField(max_length=4))
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, default=1096, on_delete=models.CASCADE)
    
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)
    
    def __str__(self):
        return str(self.user)+' ['+str(self.created)+']'


class TROPOMIYearFile(models.Model):
    year = models.CharField(max_length=4)
    location = models.CharField(max_length=200)

    def __str__(self):
        return "TROPOMI " + str(self.year)