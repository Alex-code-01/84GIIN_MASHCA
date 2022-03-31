# Generated by Django 4.0.2 on 2022-03-30 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estacion', '0005_alter_estacion_formato_alter_estacion_latitud_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estacion',
            name='formato',
            field=models.CharField(choices=[('DMS', 'Degrees Minutes Seconds'), ('DD', 'Degrees Decimal')], max_length=50, verbose_name='formato'),
        ),
    ]
