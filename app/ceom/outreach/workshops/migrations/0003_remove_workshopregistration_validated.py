# Generated by Django 2.2.13 on 2021-05-25 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0002_workshopregistration_verify_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshopregistration',
            name='validated',
        ),
    ]
