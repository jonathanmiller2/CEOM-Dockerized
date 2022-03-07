# Generated by Django 3.2.12 on 2022-03-07 02:18

import ceom.modis.visualization.models
import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('visualization', '0006_auto_20220306_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singletimeseriesjob',
            name='years',
            field=models.CharField(max_length=150, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Select years'),
        ),
        migrations.AlterField(
            model_name='timeseriesjob',
            name='points',
            field=models.FileField(max_length=150, upload_to='visualization/timeseries/input', validators=[ceom.modis.visualization.models.checkFormat], verbose_name='Upload csv file'),
        ),
        migrations.AlterField(
            model_name='timeseriesjob',
            name='years',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Select years'),
        ),
    ]
