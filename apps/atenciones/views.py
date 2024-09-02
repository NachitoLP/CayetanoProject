from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Reason, Service, Headquarter
from ..personas.models import Person
from ..organismos.models import Organism

import json

with open("secret.json") as f:
    secret = json.load(f)

@login_required
def registerAttention(request, person_dni=None):
    person = None
    
    if person_dni:
        person = get_object_or_404(Person, pk=person_dni)
    if request.method == "GET":
        return render(request, 'atenciones/register.html', {
            'reasons': Reason.objects.all(),
            'organisms': Organism.objects.all(),
            'people': Person.objects.all(),
            'personNewAttention': person,
            'headquarters': Headquarter.objects.all(),
        })
    elif request.method == "POST":
        service_reason_id = request.POST.get('service_reason_id')
        person_id = request.POST.get('person_id')
        service_description = request.POST.get('service_description')
        service_status = request.POST.get('service_status') == 'on'
        organism_id = request.POST.get('organism_id')
        service_headquarter = request.POST.get('service_headquarter')

        if not service_reason_id or not person_id or not service_description:
            return render(request, 'atenciones/register.html', {
                "error": 'No se han completado todos los datos.',
                'reasons': Reason.objects.all(),
                'organisms': Organism.objects.all(),
                'people': Person.objects.all(),
                'personNewAttention': person,
                'headquarters': Headquarter.objects.all(),
            })

        organism = None if organism_id == '' else Organism.objects.get(pk=organism_id)

        try:
            print(service_headquarter)
            new_service = Service(
                service_reason_id=Reason.objects.get(pk=service_reason_id),
                person_id=Person.objects.get(pk=person_id),
                service_description=service_description,
                service_status=service_status,
                organism_id = organism,
                service_headquarter = Headquarter.objects.get(pk=service_headquarter),
                user = request.user
            )
            new_service.save()

            return redirect('/view/attentions')

        except (Reason.DoesNotExist, Person.DoesNotExist) as e:
            return render(request, 'atenciones/register.html', {
                "error": 'Uno o más datos proporcionados son inválidos.',
                'reasons': Reason.objects.all(),
                'organisms': Organism.objects.all(),
                'people': Person.objects.all(),
                'personNewAttention': person,
                'headquarters': Headquarter.objects.all(),
            })
        except ValidationError as e:
            return render(request, 'atenciones/register.html', {
                "error": str(e),
                'reasons': Reason.objects.all(),
                'organisms': Organism.objects.all(),
                'people': Person.objects.all(),
                'personNewAttention': person,
                'headquarters': Headquarter.objects.all(),
            })

@login_required
def viewAttentions(request):
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    person_id = request.GET.get('person_id', '')
    attention_id = request.GET.get('attention_id', '')

    try:
        attentions = Service.objects.all()
        
        # Filtrar por rango de fechas
        if from_date and to_date:
            attentions = attentions.filter(service_date__range=[from_date, to_date])
        elif from_date:
            attentions = attentions.filter(service_date__gte=from_date)
        elif to_date:
            attentions = attentions.filter(service_date__lte=to_date)
        
        # Filtrar por persona atendida
        if person_id:
            attentions = attentions.filter(person_id=person_id)
        
        # Filtrar por ID de la atención
        if attention_id:
            attentions = attentions.filter(service_id=attention_id)
        
        # Obtener la lista de personas para el desplegable
        people = Person.objects.all()
        

        paginator = Paginator(attentions, 5)  # Mostrar 5 atenciones por página
        page = request.GET.get('page')  # Obtener el número de página de los parámetros de la solicitud

        try:
            attentions = paginator.page(page)
        except PageNotAnInteger:
            # Si la página no es un entero, muestra la primera página
            attentions = paginator.page(1)
        except EmptyPage:
            # Si la página está fuera del rango, muestra la última página de resultados
            attentions = paginator.page(paginator.num_pages)
        
        return render(request, 'atenciones/view.html', {
            'attentions': attentions,
            'people': people,
            'from_date': from_date,
            'to_date': to_date,
            'person_id': person_id,
            'attention_id': attention_id
        })
    except Exception as e:
        return render(request, 'atenciones/view.html', {
            'error': 'No se pudieron cargar las atenciones.',
        })

@login_required
def viewAttentionDetail(request, attention_id):
    # Obtener la atención específica o devolver un 404 si no se encuentra
    attention = get_object_or_404(Service, pk=attention_id)
    
    # Si se modifican los datos, va a recibir un método POST.
    if request.method == 'POST':
        # Obtener los datos del formulario que puedan modificarse
        service_reason_id = request.POST.get('service_reason_id')
        service_description = request.POST.get('service_description')
        service_status = 'service_status' in request.POST  # Checkbox booleano
        organism_id = request.POST.get('organism_id', None)  # Puede ser None si no se selecciona
        service_headquarter = request.POST.get('service_headquarter')

        organism = None if organism_id == '' else Organism.objects.get(pk=organism_id)
        
        # Actualizar la atención con los datos del formulario
        attention.service_reason_id = Reason.objects.get(pk=service_reason_id)
        attention.service_description = service_description
        attention.service_status = service_status
        attention.organism_id = organism
        attention.service_headquarter = Headquarter.objects.get(pk=service_headquarter)
        attention.save()

        return redirect('viewAttentionDetail', attention_id=attention.service_id)  # Redirigir para evitar reposteo

    return render(request, 'atenciones/detailView.html', {
        'attention': attention,
        'reasons': Reason.objects.all(),
        'organisms': Organism.objects.all(),
        'headquarters': Headquarter.objects.all(),
    })