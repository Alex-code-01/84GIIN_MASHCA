from django.urls import path

from . import views

urlpatterns = [
    path('', views.estaciones, name="Estaciones"),
    path('estacion/', views.estacion, name="Estacion"),
]