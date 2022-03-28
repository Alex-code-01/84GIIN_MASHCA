from multiprocessing import context
from django.shortcuts import render, HttpResponse
from Estacion.models import Estacion
import folium
from Estacion.models import Estacion
# Create your views here.

def home(request):
    return render(request, "WebApp/home.html")

def estaciones(request):    
    print("LAT, LONG")
    for e in Estacion.objects.raw('SELECT * FROM Estacion_estacion'):
        print(e.latitud, ",", e.longitud)    
    
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