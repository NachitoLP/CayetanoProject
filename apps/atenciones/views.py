from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from .models import Reason, Service
from ..personas.models import Person
from ..organismos.models import Organism

import json

with open("secret.json") as f:
    secret = json.load(f)

@login_required
def registerAtention(request):
    if request.method == "GET":
        return render(request, 'atenciones/register.html', {
            'reasons': Reason.objects.all(),
            'organisms': Organism.objects.all(),
            'people': Person.objects.all(),
        })
    elif request.method == "POST":
        service_reason_id = request.POST.get('service_reason_id')
        person_id = request.POST.get('person_id')
        service_description = request.POST.get('service_description')
        service_status = request.POST.get('service_status') == 'on'
        organism_id = request.POST.get('organism_id')

        if not service_reason_id or not person_id or not service_description:
            return render(request, 'atenciones/register.html', {
                "error": 'No se han completado todos los datos.',
                'reasons': Reason.objects.all(),
                'organisms': Organism.objects.all(),
                'people': Person.objects.all(),
            })

        organism = None if organism_id == '' else Organism.objects.get(pk=organism_id)

        try:
            new_service = Service(
                service_reason_id=Reason.objects.get(pk=service_reason_id),
                person_id=Person.objects.get(pk=person_id),
                service_description=service_description,
                service_status=service_status,
                organism_id = organism 
            )
            new_service.save()

            return redirect('/')

        except (Reason.DoesNotExist, Person.DoesNotExist) as e:
            return render(request, 'atenciones/register.html', {
                "error": 'Uno o más datos proporcionados son inválidos.',
                'reasons': Reason.objects.all(),
                'organisms': Organism.objects.all(),
                'people': Person.objects.all(),
            })
        except ValidationError as e:
            return render(request, 'atenciones/register.html', {
                "error": str(e),
                'reasons': Reason.objects.all(),
                'organisms': Organism.objects.all(),
                'people': Person.objects.all(),
            })

@login_required
def viewAtentions(request):
    try:
        attentions = Service.objects.all()
        return render(request, 'atenciones/view.html', {
            'attentions': attentions
        })
    except Exception as e:
        return render(request, 'atenciones/view.html', {
            'error': 'No se pudieron cargar las atenciones.',
        })