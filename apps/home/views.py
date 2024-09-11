from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_naive
from django.http import HttpResponse

from ..atenciones.models import Reason, Service, Headquarter

import json

import openpyxl
from openpyxl.styles import Alignment

# Create your views here.

with open("secret.json") as f:
    secret = json.load(f)

def sessionLogIn(request):
    if request.method == "GET":
        return render(request, 'login/login.html')
    elif request.method == "POST":
        if not request.POST['username'] and not request.POST['password'] :
            return render(request, 'login/login.html',{
                    "error": 'No se han completado todos los datos.'
                })
        else :
            user = authenticate(request, username = request.POST['username'] , password = request.POST['password'])
            if user is None :
                return render(request, 'login/login.html',{
                    "error": 'Los datos ingresados son incorrectos.'
                })
            else:
                login(request, user)
                return redirect(secret["SERVER_DNS"])


def sessionLogOut(request) :
    logout(request)
    return redirect(secret["SERVER_DNS"])


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener parámetros de la solicitud para estadísticas
        from_date = self.request.GET.get('from_date', '')
        to_date = self.request.GET.get('to_date', '')
        service_reason_id = self.request.GET.get('service_reason_id', '')
        headquarter_id = self.request.GET.get('headquarter_id', '')

        # Inicializar las variables para los resultados de búsqueda
        attentions = None
        total_records = 0
        show_results = False

        if from_date or to_date or service_reason_id or headquarter_id:
            attentions = Service.objects.all()

            # Filtrar por rango de fechas
            if from_date and to_date:
                attentions = attentions.filter(service_date__range=[from_date, to_date])
            elif from_date:
                attentions = attentions.filter(service_date__gte=from_date)
            elif to_date:
                attentions = attentions.filter(service_date__lte=to_date)

            # Filtrar por motivo de servicio
            if service_reason_id:
                attentions = attentions.filter(service_reason_id=service_reason_id)

            # Filtrar por sede
            if headquarter_id:
                attentions = attentions.filter(service_headquarter=headquarter_id)

            # Paginación
            paginator = Paginator(attentions, 5)  # Mostrar 5 atenciones por página
            page = self.request.GET.get('page')  # Obtener el número de página de los parámetros de la solicitud

            try:
                attentions = paginator.page(page)
            except PageNotAnInteger:
                attentions = paginator.page(1)
            except EmptyPage:
                attentions = paginator.page(paginator.num_pages)

            total_records = attentions.paginator.count
            show_results = True

        # Obtener la lista de personas y sedes para el desplegable
        headquarters = Headquarter.objects.all()
        reasons = Reason.objects.all()

        context.update({
            'attentions': attentions,
            'headquarters': headquarters,
            'reasons': reasons,
            'from_date': from_date,
            'to_date': to_date,
            'headquarter_id': headquarter_id,
            'reason_id': service_reason_id,
            'total_records': total_records,
            'show_results': show_results
        })

        return context

def export_to_excel(request):
    # Obtener parámetros de la solicitud para estadísticas
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    service_reason_id = request.GET.get('service_reason_id', '')
    headquarter_id = request.GET.get('headquarter_id', '')

    # Filtrar los datos
    attentions = Service.objects.all()

    if from_date or to_date or service_reason_id or headquarter_id:
        if from_date and to_date:
            attentions = attentions.filter(service_date__range=[from_date, to_date])
        elif from_date:
            attentions = attentions.filter(service_date__gte=from_date)
        elif to_date:
            attentions = attentions.filter(service_date__lte=to_date)
        if service_reason_id:
            attentions = attentions.filter(service_reason_id=service_reason_id)
        if headquarter_id:
            attentions = attentions.filter(service_headquarter=headquarter_id)

    # Crear un archivo Excel
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Atenciones'

    # Escribir los encabezados
    headers = ['ID', 'Motivo del Servicio', 'Sede de Atención', 'Persona Atendida', 'Organismo', 'Fecha del Servicio']
    worksheet.append(headers)
    
    column_widths = [10, 30, 30, 30, 30, 40]
    for i, width in enumerate(column_widths, start=1):
        worksheet.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width

    # Aplicar estilos
    header_font = openpyxl.styles.Font(bold=True)
    header_alignment = Alignment(horizontal='center')

    for cell in worksheet[1]:
        cell.alignment = header_alignment
        cell.font = header_font

    # Escribir los datos
    for attention in attentions:
        service_date = make_naive(attention.service_date) if attention.service_date else ''
        worksheet.append([
            attention.service_id,
            attention.service_reason_id.service_reason,
            attention.service_headquarter.headquarter_name,
            attention.person_id.person_surname + ' ' + attention.person_id.person_name,
            attention.organism_id if attention.organism_id else 'N/A',
            service_date.strftime('%d-%m-%Y %H:%M:%S') if service_date else '',
        ])
    
    for row in worksheet.iter_rows(min_row=2, max_col=worksheet.max_column, max_row=worksheet.max_row):
        for cell in row:
            cell.alignment = Alignment(horizontal='center', vertical='center')

    # Crear la respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="atenciones.xlsx"'
    workbook.save(response)
    return response