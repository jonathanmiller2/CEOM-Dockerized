# Generated by Django 2.2.13 on 2021-06-08 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gisday', '0005_remove_volunteer_v_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demographicsurvey',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gisday.Year'),
        ),
    ]
