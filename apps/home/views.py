from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from ..atenciones.models import Reason, Service, Headquarter

import json

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