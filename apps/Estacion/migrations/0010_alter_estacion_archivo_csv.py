# Generated by Django 4.0.2 on 2022-04-19 17:52

import apps.Estacion.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estacion', '0009_estacion_archivo_csv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estacion',
            name='archivo_csv',
            field=models.FileField(upload_to=apps.Estacion.models.estacion_directory_path, verbose_name='archivo_csv'),
        ),
    ]