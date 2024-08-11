from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date

from .models import Person, Province, Locality
from ..atenciones.models import Service, Reason
from ..organismos.models import Organism

import json
import datetime

with open("secret.json") as f:
    secret = json.load(f)


@login_required
def registerPerson(request):
    if request.method == "GET":
        return render(request, 'personas/register.html', {
            'provinces': Province.objects.all(),
            'localities': Locality.objects.all(),
        })
    elif request.method == "POST":
        person_dni = request.POST.get('person_dni')
        person_name = request.POST.get('person_name')
        person_surname = request.POST.get('person_surname')
        person_birthdate_str = request.POST.get('person_birthdate')
        person_address = request.POST.get('person_address')
        person_phone = request.POST.get('person_phone')
        person_bg_center = request.POST.get('person_bg_center') == 'on'
        person_observations = request.POST.get('person_observations', '')
        locality_id = request.POST.get('locality_id')
        
        if not all([person_dni, person_name, person_surname, person_birthdate_str, person_address, locality_id]):
            return render(request, 'personas/register.html', {
                "error": 'No se han completado todos los datos.',
                'provinces': Province.objects.all(),
                'localities': Locality.objects.all(),
            })
        
        try:
            person_birthdate = parse_date(person_birthdate_str)
            if not person_birthdate:
                raise ValidationError('La fecha de nacimiento no es válida.')
            if person_birthdate > datetime.date.today():
                return render(request, 'personas/register.html', {
                    "error": 'La Fecha de nacimiento no puede ser mayor a la fecha actual.',
                    'provinces': Province.objects.all(),
                    'localities': Locality.objects.all(),
                })
            
            new_person = Person(
                person_dni = person_dni,
                person_name = person_name,
                person_surname = person_surname,
                person_birthdate = person_birthdate,
                person_phone = person_phone,
                person_bg_center = person_bg_center,
                person_observations = person_observations,
                locality_id = Locality.objects.get(pk=locality_id),
            )
            new_person.save()
            
            return redirect('/')
        except Locality.DoesNotExist:
            return render(request, 'personas/register.html', {
                "error": 'Localidad no válida.',
                'provinces': Province.objects.all(),
                'localities': Locality.objects.all(),
            })
        except ValidationError as e:
            return render(request, 'personas/register.html', {
                "error": str(e),
                'provinces': Province.objects.all(),
                'localities': Locality.objects.all(),
            })

@login_required
def viewPersons(request):
    try:
        people = Person.objects.all()
        return render(request, 'personas/view.html', {
            'people': people
        })
    except Exception as e:
        return render(request, 'personas/view.html', {
            'error': 'No se pudieron cargar las personas.',
        })