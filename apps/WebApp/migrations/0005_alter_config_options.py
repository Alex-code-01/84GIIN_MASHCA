# Generated by Django 4.0.2 on 2022-05-22 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0004_alter_config_unit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='config',
            options={'verbose_name': 'configuracion', 'verbose_name_plural': 'configuraciones'},
        ),
    ]
