# Generated by Django 4.0.2 on 2022-03-30 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estacion', '0006_alter_estacion_formato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estacion',
            name='formato',
            field=models.CharField(choices=[('DMS', 'Degrees Minutes Seconds'), ('DD', 'Degrees Decimal')], default='DMS', max_length=50, verbose_name='formato'),
        ),
    ]
