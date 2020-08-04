# Generated by Django 2.2.13 on 2020-08-04 03:01

import django.core.validators
from django.db import migrations, models
import eomf.visualization.models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('visualization', '0004_auto_20150902_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singletimeseriesjob',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='singletimeseriesjob',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='singletimeseriesjob',
            name='result',
            field=models.FileField(blank=True, max_length=300, null=True, upload_to='visualization/timeseries/single'),
        ),
        migrations.AlterField(
            model_name='singletimeseriesjob',
            name='years',
            field=models.CharField(max_length=150, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Select years'),
        ),
        migrations.AlterField(
            model_name='timeseriesjob',
            name='points',
            field=models.FileField(max_length=150, upload_to='visualization/timeseries/input', validators=[eomf.visualization.models.checkFormat], verbose_name='Upload csv file'),
        ),
        migrations.AlterField(
            model_name='timeseriesjob',
            name='result',
            field=models.FileField(blank=True, max_length=300, null=True, upload_to='visualization/timeseries/multi'),
        ),
        migrations.AlterField(
            model_name='timeseriesjob',
            name='sender',
            field=models.EmailField(blank=True, max_length=150, null=True, verbose_name='Additional sender'),
        ),
        migrations.AlterField(
            model_name='timeseriesjob',
            name='years',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Select years'),
        ),
    ]
