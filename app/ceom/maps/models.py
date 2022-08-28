from django.db import models
from ceom.photos.models import Category


class GeocatterPoint(models.Model):
    id = models.AutoField(primary_key=True)
    date_categorized = models.DateTimeField(auto_now_add=True)
    lon = models.FloatField()
    lat = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)