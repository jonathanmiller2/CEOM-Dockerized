# Generated by Django 2.2.13 on 2020-08-04 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eomfshare', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='FileNew',
            field=models.FileField(upload_to='media/eomfshare'),
        ),
    ]
