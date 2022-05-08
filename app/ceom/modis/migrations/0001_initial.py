# Generated by Django 3.2.12 on 2022-02-28 20:51

import ceom.modis.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('photos', '0011_categoryvote'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('name', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('xdim', models.FloatField()),
                ('ydim', models.FloatField()),
                ('grid_size', models.FloatField()),
                ('projcode', models.IntegerField(blank=True, null=True)),
                ('zonecode', models.IntegerField(blank=True, null=True)),
                ('spherecode', models.IntegerField(blank=True, null=True)),
                ('projparm', models.CharField(blank=True, max_length=1000, null=True)),
                ('grid_name', models.CharField(blank=True, max_length=100, null=True)),
                ('ordering', models.FloatField(blank=True, null=True)),
                ('long_name', models.CharField(blank=True, max_length=100, null=True)),
                ('short_name', models.CharField(blank=True, max_length=5, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('day_res', models.IntegerField(default=8)),
                ('is_global', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('year', models.IntegerField(null=True)),
                ('day', models.IntegerField(null=True)),
                ('timestamp', models.BigIntegerField()),
                ('absolute_path', models.CharField(default='N/A', max_length=300)),
                ('dataset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='modis.dataset')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('name', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('long_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tile',
            fields=[
                ('name', models.CharField(max_length=6, primary_key=True, serialize=False)),
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
        migrations.CreateModel(
            name='TimeSeriesJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.EmailField(blank=True, max_length=150, null=True, verbose_name='Additional sender')),
                ('points', models.FileField(max_length=150, upload_to='visualization/timeseries/input', validators=[ceom.modis.models.checkFormat], verbose_name='Upload csv file')),
                ('result', models.FileField(blank=True, max_length=300, null=True, upload_to='visualization/timeseries/multi')),
                ('years', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Select years')),
                ('completed', models.BooleanField(default=False)),
                ('working', models.BooleanField(default=False)),
                ('error', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('message', models.CharField(blank=True, max_length=150, null=True)),
                ('task_id', models.CharField(blank=True, max_length=50, null=True)),
                ('total_sites', models.IntegerField(default=1)),
                ('progress', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modis.dataset')),
                ('user', models.ForeignKey(default=1096, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SingleTimeSeriesJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(blank=True, max_length=50, null=True)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('row', models.IntegerField(blank=True, null=True)),
                ('col', models.IntegerField(blank=True, null=True)),
                ('tile', models.CharField(blank=True, max_length=6, null=True)),
                ('result', models.FileField(blank=True, max_length=300, null=True, upload_to='visualization/timeseries/single')),
                ('years', models.CharField(max_length=150, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Select years')),
                ('completed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modis.dataset')),
                ('user', models.ForeignKey(default=1096, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(blank=True, null=True, verbose_name='date processed')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='modis.file')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='modis.product')),
            ],
        ),
        migrations.CreateModel(
            name='GeocatterPoint',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_categorized', models.DateTimeField(auto_now_add=True)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photos.category')),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='products',
            field=models.ManyToManyField(through='modis.Process', to='modis.Product'),
        ),
        migrations.AddField(
            model_name='file',
            name='tile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modis.tile'),
        ),
    ]
