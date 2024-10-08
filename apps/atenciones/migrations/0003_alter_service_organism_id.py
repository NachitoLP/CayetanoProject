# Generated by Django 5.0.7 on 2024-08-10 23:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atenciones', '0002_alter_service_options'),
        ('organismos', '0002_alter_organism_organism_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='organism_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='organismos.organism', verbose_name='Organismo interviniente'),
        ),
    ]
