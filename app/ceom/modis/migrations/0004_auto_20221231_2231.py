# Generated by Django 3.2.16 on 2022-12-31 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modis', '0003_auto_20221220_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='modismultipletimeseriesjob',
            name='dataset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='modis.dataset'),
        ),
        migrations.AddField(
            model_name='modissingletimeseriesjob',
            name='dataset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='modis.dataset'),
        ),
    ]
