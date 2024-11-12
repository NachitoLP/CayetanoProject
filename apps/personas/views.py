from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.db.models import Q
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Person, Province, Locality
from ..atenciones.models import Service, Reason
from ..organismos.models import Organism

from datetime import datetime, date

def validate_birthdate(person_birthdate_str):
    try:
        # Cambiar el formato a '%Y-%m-%d' para analizar correctamente la fecha.
        person_birthdate = datetime.strptime(person_birthdate_str, '%Y-%m-%d').date()
    except ValueError:
        raise ValidationError('La fecha de nacimiento no es válida.')

    if person_birthdate > date.today():
        raise ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual.')

    return person_birthdate

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
        
        if not all([person_dni, person_name, person_surname, person_birthdate_str, locality_id, person_phone]):
            return render(request, 'personas/register.html', {
                "error": 'No se han completado todos los datos.',
                'provinces': Province.objects.all(),
                'localities': Locality.objects.all(),
            })
            
        #DNI YA REGISTRADO
        if Person.objects.filter(person_dni=person_dni).exists():
            return render(request, 'personas/register.html', {
                'error': 'El DNI ya está registrado.',
                'provinces': Province.objects.all(),
                'localities': Locality.objects.all(),
            })
        try:
            if person_birthdate_str:
                try:
                    # Validamos la fecha de nacimiento
                    person_birthdate = validate_birthdate(person_birthdate_str)
                except ValidationError as e:
                    return render(request, 'personas/register.html', {
                        'error': str(e),  # El mensaje de error personalizado
                        'provinces': Province.objects.all(),
                        'localities': Locality.objects.all(),
                })
            
            new_person = Person(
                person_dni = person_dni,
                person_name = person_name,
                person_surname = person_surname,
                person_birthdate = person_birthdate,
                person_address = person_address,
                person_phone = person_phone,
                person_bg_center = person_bg_center,
                person_observations = person_observations,
                locality_id = Locality.objects.get(pk=locality_id),
                created_at = timezone.now(),
            )
            new_person.save()
            
            return redirect(f'/view/persons/{new_person.person_dni}')
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
        except IntegrityError:
            return render(request, 'personas/register.html', {
                'error': 'Hubo un error al guardar la persona. Intenta de nuevo.',
                'provinces': Province.objects.all(),
                'localities': Locality.objects.all(),
            })


@login_required
def viewPersons(request):
    query = request.GET.get('query', '')
    try:
        if query:
            people = Person.objects.filter(
                Q(person_dni__istartswith=query) | Q(person_surname__istartswith=query)
            ) #Se hace un filtrado tanto por DNI como por Apellido, y el __istartswith hace una búsqueda insensible a mayúsculas y minúsculas
        else:
            # Si no hay término de búsqueda, muestra todos los registros
            people = Person.objects.all().order_by('-created_at')


        paginator = Paginator(people, 5)  # Mostrar 5 personas por página
        page = request.GET.get('page')  # Obtener el número de página de los parámetros de la solicitud

        try:
            people = paginator.page(page)
        except PageNotAnInteger:
            # Si la página no es un entero, muestra la primera página
            people = paginator.page(1)
        except EmptyPage:
            # Si la página está fuera del rango, muestra la última página de resultados
            people = paginator.page(paginator.num_pages)
        
        return render(request, 'personas/view.html', {
            'people': people,
            'query': query
        })
    except Exception as e:
        return render(request, 'personas/view.html', {
            'error': 'No se pudieron cargar las personas.',
        })

@login_required
def viewPersonDetail(request, person_dni):
    # Obtener la persona a partir del DNI.
    person = get_object_or_404(Person, pk=person_dni)
    attentions = Service.objects.filter(person_id=person_dni)
    paginator = Paginator(attentions, 5)
    page = request.GET.get('page')

    try:
        attentions = paginator.page(page)
    except PageNotAnInteger:
        attentions = paginator.page(1)
    except EmptyPage:
        attentions = paginator.page(paginator.num_pages)
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        new_person_dni = request.POST.get('person_dni')
        person_name = request.POST.get('person_name')
        person_surname = request.POST.get('person_surname')
        person_birthdate_str = request.POST.get('person_birthdate')
        person_address = request.POST.get('person_address')
        person_phone = request.POST.get('person_phone')
        person_bg_center = request.POST.get('person_bg_center') == 'on'
        person_observations = request.POST.get('person_observations', '')
        locality_id = request.POST.get('locality_id')
        
        if not all([new_person_dni, person_name, person_surname, person_birthdate_str, locality_id]):
            return render(request, 'personas/detailView.html', {
                "error": 'No se han completado todos los datos.',
                "person": person,
                "attentions": attentions,
                'provinces': Province.objects.all(),
                'localities': Locality.objects.all(),
            })

        # Si el DNI ha cambiado, verificamos si ya existe en la base de datos
        if new_person_dni != str(person.person_dni):
            if Person.objects.filter(person_dni=new_person_dni).exists():
                return render(request, 'personas/detailView.html', {
                    "error": 'El DNI ya está registrado.',
                    "person": person,
                    "attentions": attentions,
                    'provinces': Province.objects.all(),
                    'localities': Locality.objects.all(),
                })

        try:
            if person_birthdate_str:
                try:
                    # Validamos la fecha de nacimiento
                    print(person_birthdate_str)
                    person_birthdate = validate_birthdate(person_birthdate_str)
                except ValidationError as e:
                    return render(request, 'personas/register.html', {
                        'error': str(e),  # El mensaje de error personalizado
                        'provinces': Province.objects.all(),
                        'localities': Locality.objects.all(),
                    })

            # Si todo está bien, actualizar los datos
            person.person_dni = new_person_dni  # Solo actualizar si el DNI ha cambiado
            person.person_name = person_name
            person.person_surname = person_surname
            person.person_birthdate = person_birthdate
            person.person_address = person_address
            person.person_phone = person_phone
            person.person_bg_center = person_bg_center
            person.person_observations = person_observations
            person.locality_id = Locality.objects.get(pk=locality_id)

            person.save()

            return redirect('viewPersonDetail', person_dni=person.person_dni)
    
        except ValidationError as e:
            return render(request, 'personas/detailView.html', {
                "error": str(e),
                "person": person,
                "attentions": attentions,
                'provinces': Province.objects.all(),
                'localities': Locality.objects.all(),
            })
    return render(request, 'personas/detailView.html', {
        "person": person,
        "attentions": attentions,
        'provinces': Province.objects.all(),
        'localities': Locality.objects.all(),
    })
