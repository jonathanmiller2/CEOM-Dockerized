# Generated by Django 2.2.13 on 2021-05-25 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopregistration',
            name='verify_email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]