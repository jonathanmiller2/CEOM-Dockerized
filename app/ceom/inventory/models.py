#This class describes the inventory data model in Django
# model syntax

from django.db import models
import datetime

class Dataset(models.Model):
    name = models.CharField(max_length=7, primary_key=True)
    xdim = models.FloatField()
    ydim = models.FloatField()
    grid_size = models.FloatField()
    projcode = models.IntegerField()
    zonecode = models.IntegerField()
    spherecode = models.IntegerField()
    projparm = models.CharField(max_length=1000)
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

class TileManager(models.Manager):
    def with_count(self, product, year):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT t.name,t.ih,t.iv, count(*) "+
                       "FROM inventory_tile as t, inventory_file as f "+
                       "WHERE t.name = f.tile_id "+
                       "AND f.year = "+year+" AND f.dataset_id = '"+product+"' group by 1,2,3")
        result_list = []
        for row in cursor.fetchall():
            p = self.model(name=row[0],ih=row[1],iv=row[2])
            p.count = int(row[3])
            result_list.append(p)
        return result_list

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

    objects = TileManager()    

    def toString(self):
        return self.name + ";ih=" + str(self.ih) + ";long_min=" \
               + str(self.lon_min) +";" + self.continent + ";"

    def __str__(self):
        return self.name
        
class File(models.Model):
    tile = models.ForeignKey(Tile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    year = models.IntegerField(null=True)
    day = models.IntegerField(null=True)
    timestamp = models.IntegerField()
    dataset = models.ForeignKey(Dataset, null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='Process')
    absolute_path = models.CharField(max_length = 300, null=False, default='N/A')
    def __str__(self):
        return self.name

class Process(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField('date processed', null=True, blank=True)
