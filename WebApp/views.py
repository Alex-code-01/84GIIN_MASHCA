from multiprocessing import context
from django.shortcuts import render, HttpResponse
import folium

# Create your views here.

def home(request):
    return render(request, "WebApp/home.html")

def estaciones(request):
    m = folium.Map()
    m = m._repr_html_()
    context = {
        'm': m,
    }
    return render(request, "WebApp/estaciones.html", context)

def contacto(request):
    return render(request, "WebApp/contacto.html")

def login(request):
    return render(request, "WebApp/login.html")