from django.db import models
from ceom.photos.models import Category


class GeocatterPoint(models.Model):
    id = models.AutoField(primary_key=True)
    date_categorized = models.DateTimeField(auto_now_add=True)
    date_taken = models.DateTimeField(null=False)
    lon = models.FloatField(null=False)
    lat = models.FloatField(null=False)
    is_multi_cat = models.BooleanField(null=False)
    primary_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    secondary_category = models.ForeignKey(Category, on_delete=models.CASCADE)