from django.contrib.gis.db import models
from django import forms
from django.conf import settings
from ceom.modis.models import Dataset
import time

class Datatype(models.Model):
    name = models.CharField(max_length=10, primary_key=True, unique=True)
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
        
class Datainfo(models.Model):
    name = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    abstract = models.TextField(blank=True)
    label = models.CharField(max_length=100)
    legend = models.BooleanField()
    vector = models.BooleanField()
    datatype = models.ForeignKey(Datatype, null=True, blank=True, on_delete=models.CASCADE)
    source = models.CharField(max_length=100,blank=True, null=True)
    order = models.IntegerField(blank=True,null=True)
    
    #class Meta:
    #    db_table = u'map_dataset'
    
    def __str__(self):
        return self.name

class H5n1(models.Model):
    id = models.IntegerField(primary_key=True)
    region = models.CharField(max_length=25)
    country = models.CharField(max_length=64)
    admin1 = models.CharField(max_length=64)
    admin2 = models.CharField(max_length=64, null=True)
    quality = models.CharField(max_length=64, null=True)
    locality = models.CharField(max_length=86)
    latitude = models.DecimalField(max_digits=10, decimal_places=5)
    longitude = models.DecimalField(max_digits=10, decimal_places=5)
    observation_date = models.DateField()
    surveillance_type = models.CharField(max_length=20)
    reporting_date = models.DateField()
    diagnosis_status = models.CharField(max_length=20)
    disease = models.CharField(max_length=40)
    disease_type = models.CharField(max_length=4, null=True)
    species = models.CharField(max_length=256, null = True)
    at_risk = models.IntegerField(null=True)
    cases = models.IntegerField(null=True)
    deaths = models.IntegerField(null=True)
    destroyed = models.IntegerField(null=True)
    slaughtered = models.IntegerField(null=True)
    vaccinated = models.IntegerField(null=True)
    location = models.PointField()


    def __str__(self):
        return "Case: "+str(self.id)
    
    def name(self):
        return "Case: "+str(self.id)
    
    def description(self):
        items = ["Region: "+str(self.region), 
                 "Observed on: "+str(self.observation_date),
                 "Reported on: "+str(self.reporting_date),
                 "Disease: "+str(self.disease)
                ]
        return "\n".join(items)
        
    def timespan(self):
        str = self.observation_date.strftime("%Y-%m-%dT%H:%M:%S")
        return {'begin': str, 'end': str}
        
class Birds(models.Model):
    duty = models.IntegerField(null=True, blank=True)            # 99
    spp = models.CharField(max_length=16, null=True, blank=True) # Swan Goose
    month = models.IntegerField(null=True, blank=True)           # 10
    dutylocs = models.IntegerField(null=True, blank=True)        # 8
    second = models.IntegerField(null=True, blank=True)          # 0
    lc94 = models.CharField(max_length=2, null=True, blank=True) # LG
    mmdd = models.CharField(max_length=5, null=True, blank=True) # 10_12
    year = models.IntegerField(null=True, blank=True)            # 2008
    jday = models.IntegerField(null=True, blank=True)            # 286
    ptt = models.IntegerField(null=True, blank=True)             # 82105
    deplylon = models.FloatField(null=True, blank=True)          # 114.641
    gspeed = models.CharField(max_length=3, null=True, blank=True) #
    gmt_min = models.IntegerField(null=True, blank=True)         # 0
    deltahr = models.FloatField(null=True, blank=True)           # 8.00
    source = models.CharField(max_length=3, null=True, blank=True) # gps
    longitud = models.FloatField(null=True, blank=True)          # 124.4015
    animal = models.CharField(max_length=14, null=True, blank=True) # SG08_82105
    latitude = models.FloatField(null=True, blank=True)          # 39.8365
    gazm = models.CharField(max_length=3, null=True, blank=True) #
    gmt_sec = models.IntegerField(null=True, blank=True)         # 0
    ghour = models.IntegerField(null=True, blank=True)           # 4
    ddmm = models.CharField(max_length=5, null=True, blank=True) # 12_10
    gmt_hour = models.IntegerField(null=True, blank=True)        # 4
    gmin = models.IntegerField(null=True, blank=True)            # 0
    dtime = models.CharField(max_length=16, null=True, blank=True) # 06JUL08:00:00:01
    gmt_date = models.CharField(max_length=10, null=True, blank=True) # 10/12/2008
    deplylat = models.FloatField(null=True, blank=True)          # 49.731
    jd = models.IntegerField(null=True, blank=True)              # 8286
    line = models.CharField(max_length=32, null=True, blank=True) # SG08_8210520081012:040000GPS
    day = models.IntegerField(null=True, blank=True)             # 12
    minute = models.IntegerField(null=True, blank=True)          # 0
    gelev = models.IntegerField(null=True, blank=True)           # -9999
    distance = models.FloatField(null=True, blank=True)          # 3.80
    hour = models.IntegerField(null=True, blank=True)            # 4
    rate = models.FloatField(null=True, blank=True)              # 0.48
    nlocrank = models.FloatField(null=True, blank=True)          # 70000.00
    daysdply = models.IntegerField(null=True, blank=True)        # 98
    thetime = models.CharField(max_length=16, null=True, blank=True) # 12OCT08:04:00:00
    azimuth = models.FloatField(null=True, blank=True)           # 108.82
    latest = models.IntegerField(null=True, blank=True)          # 0
    first = models.IntegerField(null=True, blank=True)           # 0
    location = models.PointField(null=True)
    
    
    def __str__(self):
        return "Animal: "+str(self.animal)
    
    def timeString(self):
        t = (self.year,self.month,self.day,self.ghour,self.minute,self.gmt_sec)
        return "%s-%02d-%02dT%02d:%02d:%02d" % t 
    
    def name(self):
        return "Animal: "+str(self.animal)
    
    def description(self):
        items = ["Specie: "+str(self.spp), 
                 "Observed on: "+str(self.thetime),
                ]
        return "\n".join(items)
        
    def timespan(self):
        str = self.timeString()
        return {'begin': str, 'end': str}


def single_day_birds():
    objects = Birds.objects.order_by("animal","gmt_date").distinct("animal","gmt_date").kml()
    styles = [{'name':'default', 'color':'8800ff00', 'icon':'http://ceom.ou.edu/static/images/icons/goose-icon.png'}]
    return objects, styles