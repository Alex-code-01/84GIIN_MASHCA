from multiprocessing import context
from django.shortcuts import render, HttpResponse
from Estacion.models import Estacion
import folium
from Estacion.models import Estacion
from Estacion.modules import estacion_funciones as ef
# Create your views here.

def home(request):
    return render(request, "WebApp/home.html")

def estaciones(request):    
    m = folium.Map(location=[-1.671743709620801, -78.660423157757], zoom_start=6)
    for e in Estacion.objects.raw('SELECT * FROM Estacion_estacion'):
        #print(e.latitud, ",", e.longitud) 
        #print(ef.conv_DMS_a_DD(e.latitud), ",", ef.conv_DMS_a_DD(e.longitud))  
        folium.Marker([ef.conv_DMS_a_DD(e.latitud), ef.conv_DMS_a_DD(e.longitud)], tooltip='Selecciona para visualizar', popup=e.nombre).add_to(m) 

    m = m._repr_html_()
    context = {
        'm': m,
    }
    return render(request, "WebApp/estaciones.html", context)

def contacto(request):
    return render(request, "WebApp/contacto.html")

def login(request):
    return render(request, "WebApp/login.html")