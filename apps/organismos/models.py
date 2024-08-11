from django.db import models
from auditlog.registry import auditlog

class Organism(models.Model):
    organism_id = models.AutoField('ID Organismo', primary_key=True)
    organism_name = models.CharField('Nombre del Organismo', max_length=50)
    organism_description = models.TextField('Descripción', blank=True)
    
    class Meta:
        ordering = ['organism_name']
        verbose_name = 'Organismo'
        verbose_name_plural = 'Organismos'
    
    def __str__(self):
        return self.organism_name

auditlog.register(Organism)