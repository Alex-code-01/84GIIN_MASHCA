# Generated by Django 4.0.2 on 2022-05-17 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0004_usuario_groups_usuario_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
