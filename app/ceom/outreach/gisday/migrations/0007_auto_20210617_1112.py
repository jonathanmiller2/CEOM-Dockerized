# Generated by Django 2.2.18 on 2021-06-17 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gisday', '0006_auto_20210617_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='citizenship',
            field=models.CharField(max_length=50, verbose_name='Citizenship'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='ethnicity',
            field=models.CharField(max_length=50, verbose_name='Ethnicity'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='gender',
            field=models.CharField(max_length=50, verbose_name='Gender'),
        ),
    ]
