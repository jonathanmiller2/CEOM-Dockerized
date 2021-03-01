#from django.db import models
from django.contrib.gis.db import models

# Create your models here.
class DuckTrack(models.Model):
    gid = models.IntegerField(primary_key=True)
    animal = models.CharField(max_length=20)
    ptt = models.CharField(max_length=15)
    record_id = models.CharField(max_length=30)
    datetime = models.DateTimeField()
    days_ago = models.IntegerField()
    latitude = models.DecimalField(max_digits=10, decimal_places=3)
    longitude = models.DecimalField(max_digits=10, decimal_places=3)
    lc94 = models.CharField(max_length=6)
    nmess = models.IntegerField()
    days_dply = models.IntegerField()
    sen1 = models.IntegerField()
    sen2 = models.IntegerField()
    sen3 = models.IntegerField()
    sen4 = models.IntegerField()
    location = models.PointField()
    

    def __str__(self):
        return str(self.gid)
    
    class Meta:
        db_table = 'duck_tracks'

class DuckTrackLine(models.Model):
    gid = models.IntegerField(primary_key=True)
    animal = models.CharField(max_length=20)
    location = models.LineStringField()
    

    def __str__(self):
        return (self.gid)
    
    class Meta:
        db_table = 'duck_track_line'
