from django.db import models
from ceom.photos.models import Category
from django.contrib.auth.models import User
from django.contrib.gis.db import models


class GeocatterPoint(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    date_categorized = models.DateField(auto_now_add=True)
    date_taken = models.DateField(null=False)
    grid_npix = models.IntegerField(null=False)
    tile_h = models.IntegerField(null=False)
    tile_v = models.IntegerField(null=False)
    pixel_x = models.IntegerField(null=False)
    pixel_y = models.IntegerField(null=False)
    center = models.PointField(null=False, srid=4326)
    is_multi_cat = models.BooleanField(null=False)
    primary_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="primary_category")
    secondary_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="secondary_category", null=True)