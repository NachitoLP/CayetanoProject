"""
URL configuration for cayetanoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.home.views import IndexView, sessionLogIn, sessionLogOut
from apps.estadisticas.views import StatisticsView, export_to_excel
from apps.atenciones.views import registerAttention, viewAttentions, viewAttentionDetail
from apps.personas.views import registerPerson, viewPersons, viewPersonDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('statistics/', StatisticsView.as_view() , name='statistics'),
    path('statistics/export', export_to_excel, name='export_to_excel'),
    path('sign-in/', sessionLogIn),
    path('log-out/', sessionLogOut),
    path('register/attention', registerAttention, name='registerAttention'),
    path('register/attention/<int:person_dni>/', registerAttention, name='registerAttention'),
    path('view/attentions', viewAttentions),
    path('view/attentions/<int:attention_id>', viewAttentionDetail, name='viewAttentionDetail'),
    path('register/person', registerPerson),
    path('view/persons', viewPersons),
    path('view/persons/<int:person_dni>', viewPersonDetail, name='viewPersonDetail')
]
