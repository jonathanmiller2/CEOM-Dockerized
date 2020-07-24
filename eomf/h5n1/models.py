from django.contrib.gis.db import models

class Case(models.Model):
    id = models.IntegerField(primary_key=True)
    region = models.CharField(max_length=25)
    country = models.CharField(max_length=64)
    admin1 = models.CharField(max_length=64)
    admin2 = models.CharField(max_length=64, null=True)
    locality = models.CharField(max_length=86)
    latitude = models.DecimalField(max_digits=10, decimal_places=5)
    longitude = models.DecimalField(max_digits=10, decimal_places=5)
    observation_date = models.DateField()
    surveillance_type = models.CharField(max_length=20)
    reporting_date = models.DateField()
    diagnosis_status = models.CharField(max_length=20)
    disease = models.CharField(max_length=40)
    virus = models.CharField(max_length=5)
    animal_type = models.CharField(max_length=25)
    animal_class = models.CharField(max_length=25)
    species = models.CharField(max_length=86, null = True)
    at_risk = models.IntegerField(null=True)
    cases = models.IntegerField(null=True)
    deaths = models.IntegerField(null=True)
    destroyed = models.IntegerField(null=True)
    slaughtered = models.IntegerField(null=True)
    location = models.PointField()

    def __unicode__(self):
        return "Case: "+str(self.id)
