# Generated by Django 5.0.9 on 2024-11-12 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atenciones', '0010_headquarter_headquarter_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service_description',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción de la atención'),
        ),
    ]