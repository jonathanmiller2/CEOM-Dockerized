# Generated by Django 3.2.4 on 2021-07-04 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aboutus', '0009_alter_person_headshot'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]