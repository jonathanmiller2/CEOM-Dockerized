# Generated by Django 2.2.20 on 2021-06-07 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0005_auto_20210607_0356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='id_prim',
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]