from django.urls import path

from . import views

urlpatterns = [
    path('', views.estaciones, name="Estaciones"),
    path('estacion/<str:codigo>', views.estacion, name="Estacion"),
    path('historico', views.historico, name="Historico"),
]