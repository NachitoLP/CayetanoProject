from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

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

class IndexView (LoginRequiredMixin,TemplateView):
    template_name = 'home/index.html'