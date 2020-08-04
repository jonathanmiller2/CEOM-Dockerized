# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('name', models.CharField(max_length=7, serialize=False, primary_key=True)),
                ('xdim', models.FloatField()),
                ('ydim', models.FloatField()),
                ('grid_size', models.FloatField()),
                ('projcode', models.IntegerField()),
                ('zonecode', models.IntegerField()),
                ('spherecode', models.IntegerField()),
                ('projparm', models.CharField(max_length=1000)),
                ('grid_name', models.CharField(max_length=100, null=True, blank=True)),
                ('ordering', models.FloatField(null=True, blank=True)),
                ('long_name', models.CharField(max_length=100, null=True, blank=True)),
                ('short_name', models.CharField(max_length=5, null=True, blank=True)),
                ('location', models.CharField(max_length=100, null=True, blank=True)),
                ('day_res', models.IntegerField(default=8)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('year', models.IntegerField(null=True)),
                ('day', models.IntegerField(null=True)),
                ('timestamp', models.IntegerField()),
                ('absolute_path', models.CharField(default=b'N/A', max_length=300)),
                ('dataset', models.ForeignKey(to='inventory.Dataset', null=True, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(null=True, verbose_name=b'date processed', blank=True)),
                ('file', models.ForeignKey(to='inventory.File', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('name', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('long_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tile',
            fields=[
                ('name', models.CharField(max_length=6, serialize=False, primary_key=True)),
                ('upleftx', models.FloatField(null=True)),
                ('uplefty', models.FloatField(null=True)),
                ('lowrightx', models.FloatField(null=True)),
                ('lowrighty', models.FloatField(null=True)),
                ('iv', models.IntegerField()),
                ('ih', models.IntegerField()),
                ('lon_min', models.FloatField(null=True)),
                ('lon_max', models.FloatField(null=True)),
                ('lat_min', models.FloatField(null=True)),
                ('lat_max', models.FloatField(null=True)),
                ('continent', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='process',
            name='product',
            field=models.ForeignKey(to='inventory.Product', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='file',
            name='products',
            field=models.ManyToManyField(to='inventory.Product', null=True, through='inventory.Process'),
        ),
        migrations.AddField(
            model_name='file',
            name='tile',
            field=models.ForeignKey(to='inventory.Tile',on_delete=models.CASCADE),
        ),
    ]
