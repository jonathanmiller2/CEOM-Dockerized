# Generated by Django 3.2.16 on 2022-12-25 05:11

from django.db import migrations, models
import django.db.models.deletion
from ceom.modis.models import *


class Migration(migrations.Migration):
    ds = Dataset.objects.get(name="MOD09A1")

    dependencies = [
        ('modis', '0003_auto_20221220_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='modismultipletimeseriesjob',
            name='dataset',
            field=models.ForeignKey(default=ds, on_delete=django.db.models.deletion.CASCADE, to='modis.dataset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modissingletimeseriesjob',
            name='dataset',
            field=models.ForeignKey(default=ds, on_delete=django.db.models.deletion.CASCADE, to='modis.dataset'),
            preserve_default=False,
        ),
    ]
