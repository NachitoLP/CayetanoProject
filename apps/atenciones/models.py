from django.db import models
from django.utils.timezone import localtime

from ..personas.models import Person
from ..organismos.models import Organism

from auditlog.registry import auditlog

import datetime

class Reason(models.Model):
    service_reason_id = models.AutoField('ID Motivo', primary_key= True)
    service_reason = models.CharField('Motivo', max_length=50)
    
    class Meta:
        ordering = ['service_reason']
        verbose_name = 'Motivo'
        verbose_name_plural = 'Motivos'
    
    def __str__(self):
        return self.service_reason

auditlog.register(Reason)

class Service(models.Model):
    service_id = models.AutoField('ID Atencion', primary_key=True)
    service_reason_id = models.ForeignKey(Reason,on_delete=models.CASCADE, verbose_name='Motivo')
    service_date = models.DateTimeField('Fecha de registro', auto_now_add=True)
    service_modified_date = models.DateTimeField('Fecha de modificación', auto_now=True)
    service_status = models.BooleanField('¿Se desarrolló el seguimiento correspondiente?')
    service_description = models.TextField('Descripción de la atención')
    organism_id = models.ForeignKey(Organism,on_delete=models.CASCADE, verbose_name='Organismo interviniente', null=True, blank=True)
    person_id = models.ForeignKey(Person,on_delete=models.CASCADE, verbose_name='Persona atendida')
    
    class Meta:
        ordering = ['-service_date']
        verbose_name = 'Atención'
        verbose_name_plural = 'Atenciones'
    
    def formatted_service_date(self):
        return self.service_date.strftime('%d-%m-%Y %H:%M:%S')
    
    def formatted_service_modified_date(self):
        return self.service_modified_date.strftime('%d-%m-%Y %H:%M:%S')
    
    formatted_service_date.short_description = 'Fecha de Atención'
    formatted_service_modified_date.short_description = 'Fecha de Modificación'
    
    def __str__(self):
        local_time = localtime(self.service_date)
        return f'{local_time.strftime("%d-%m-%Y %H:%M:%S")} - {self.person_id}'

auditlog.register(Service)