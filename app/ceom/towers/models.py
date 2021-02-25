from django.db import models

class phenocam(models.Model):
	sitename = models.CharField(max_length=50, blank=True)
	takendate = models.DateTimeField(null=True, blank=True)
	red = models.DecimalField(max_digits=20, decimal_places=18, null=True, blank=True)
	green = models.DecimalField(max_digits=20, decimal_places=18, null=True, blank=True)
	blue = models.DecimalField(max_digits=20, decimal_places=18, null=True, blank=True)
	gcc = models.DecimalField(max_digits=20, decimal_places=18, null=True, blank=True)
# Create your models here.
