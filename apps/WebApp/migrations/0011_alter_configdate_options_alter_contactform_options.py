# Generated by Django 4.0.2 on 2022-06-08 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0010_alter_contactform_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='configdate',
            options={'verbose_name': 'Configuracion_Fecha', 'verbose_name_plural': 'Configuraciones_Fechas'},
        ),
        migrations.AlterModelOptions(
            name='contactform',
            options={'verbose_name': 'Contacto_Mensaje', 'verbose_name_plural': 'Contacto_Mensajes'},
        ),
    ]
