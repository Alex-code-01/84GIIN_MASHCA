from django.urls import path

from . import views

urlpatterns = [
    path('', views.estaciones, name="Estaciones"),
    path('', views.estacion, name="Estacion"),
]