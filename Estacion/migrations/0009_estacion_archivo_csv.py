# Generated by Django 4.0.2 on 2022-04-19 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estacion', '0008_datoscalamaca'),
    ]

    operations = [
        migrations.AddField(
            model_name='estacion',
            name='archivo_csv',
            field=models.FileField(default=None, upload_to='', verbose_name='archivo_csv'),
            preserve_default=False,
        ),
    ]