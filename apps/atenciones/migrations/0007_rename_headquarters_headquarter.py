# Generated by Django 5.0.7 on 2024-09-01 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atenciones', '0006_headquarters_service_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Headquarters',
            new_name='Headquarter',
        ),
    ]