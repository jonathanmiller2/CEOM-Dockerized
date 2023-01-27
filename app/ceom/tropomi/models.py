from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

class TROPOMISingleTimeSeriesJob(models.Model):
    # task_id: unique id from celery updated upon task start
    task_id = models.CharField(null=True,blank=True,max_length=50)
    pixelx = models.IntegerField(blank=True, null=True)
    pixely = models.IntegerField(blank=True, null=True)
    result = models.FileField(upload_to='tropomi/timeseries/single', blank=True,null=True,max_length=300)
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

class TROPOMIMultipleTimeSeriesJob(models.Model):
    # task_id: unique id from celery updated upon task start
    task_id = models.CharField(null=True,blank=True,max_length=50)
    points = models.FileField(upload_to='tropomi/timeseries/multi/input/', max_length=150)
    result = models.FileField(upload_to='tropomi/timeseries/multi/output/', blank=True, null=True, max_length=300)
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


class TROPOMIYearFile(models.Model):
    year = models.CharField(max_length=4)
    location = models.CharField(max_length=200)

    def __str__(self):
        return "TROPOMI " + str(self.year)