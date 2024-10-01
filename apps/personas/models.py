from django.db import models
from auditlog.registry import auditlog
from datetime import date


class Province (models.Model) :
    province_id = models.AutoField('ID Provincia', primary_key=True)
    province_name = models.CharField('Nombre Provincia', max_length=35)
    
    class Meta:
        ordering = ['province_name']
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
    
    def __str__(self):
        return self.province_name


class Locality (models.Model) :
    locality_id = models.AutoField('ID Localidad', primary_key=True)
    locality_name = models.CharField('Nombre Localidad', max_length=40)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name='Provincia')
    
    class Meta:
        ordering = ['locality_name']
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'
    
    def __str__(self):
        return self.locality_name

class Person (models.Model) :
    person_dni = models.IntegerField('DNI', primary_key=True, unique=True)
    person_name = models.CharField('Nombre' , max_length=50)
    person_surname = models.CharField('Apellido' , max_length=50)
    person_birthdate = models.DateField('Fecha de nacimiento')
    person_address = models.CharField('Dirección', max_length=100)
    person_phone = models.IntegerField('Teléfono')
    person_bg_center = models.BooleanField('¿Pertenece al Centro de abuelos?')
    person_observations = models.TextField('Observaciones', blank=True)
    locality_id = models.ForeignKey(Locality, on_delete=models.CASCADE, verbose_name='Localidad')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['person_surname','person_name']
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
    
    def __str__(self):
        return f"{self.person_surname} {self.person_name} - {self.person_dni}"
    
    def age(self):
        today = date.today()
        age = today.year - self.person_birthdate.year - ((today.month, today.day) < (self.person_birthdate.month, self.person_birthdate.day))
        return age

auditlog.register(Province)
auditlog.register(Person)
auditlog.register(Locality)
