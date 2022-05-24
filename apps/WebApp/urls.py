from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="Home"),    
    path('contacto/', views.contacto, name="Contacto"),    
]