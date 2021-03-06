# Generated by Django 2.2.20 on 2021-06-07 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0004_auto_20210607_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='dir_card',
            field=models.CharField(blank=True, choices=[('N', 'North'), ('NNE', 'NNE'), ('NE', 'NE'), ('ENE', 'ENE'), ('E', 'East'), ('ESE', 'ESE'), ('SE', 'SE'), ('SSE', 'SSE'), ('S', 'South'), ('SSW', 'SSW'), ('SW', 'SW'), ('WSW', 'WSW'), ('W', 'West'), ('WNW', 'WNW'), ('NW', 'NW'), ('NNW', 'NNW')], db_column='dir', max_length=4, null=True),
        ),
    ]
