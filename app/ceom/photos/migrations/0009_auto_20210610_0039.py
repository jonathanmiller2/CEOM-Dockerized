# Generated by Django 2.2.20 on 2021-06-10 00:39

import ceom.photos.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0008_auto_20210607_0442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(blank=True, db_column='location', max_length=300, storage=django.core.files.storage.FileSystemStorage(base_url='/media/photos/', location='/code/ceom/media/photos'), upload_to=ceom.photos.models.photo_path),
        ),
    ]
