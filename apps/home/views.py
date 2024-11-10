from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_naive
from django.http import HttpResponse

from ..atenciones.models import Reason, Service, Headquarter

import os
import openpyxl
from openpyxl.styles import Alignment


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
                return redirect('http://127.0.0.1:8000/')#(os.getenv('SERVER_DNS') or 'http://127.0.0.1:8000/')


def sessionLogOut(request) :
    logout(request)
    return redirect(os.getenv('SERVER_DNS') or 'http://127.0.0.1:8000/')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'home/index.html'