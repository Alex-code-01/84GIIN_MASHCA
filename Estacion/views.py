from django.shortcuts import render

import folium
from Estacion.models import Estacion
from Estacion.modules import estacion_funciones as ef
# Create your views here.

def estaciones(request):    
    m = folium.Map(location=[-1.671743709620801, -78.660423157757], zoom_start=6)
    for e in Estacion.objects.raw('SELECT * FROM Estacion_estacion'):                
        folium.Marker(
            [ef.conv_DMS_a_DD(e.latitud), ef.conv_DMS_a_DD(e.longitud)], 
            tooltip='Selecciona para visualizar', 
            popup='<b>Estación: </b><a href=# class=linksEstaciones>' + e.nombre + '</a>',
            icon=folium.Icon(icon="cloud"),          
        ).add_to(m) 

    m = m._repr_html_()
    context = {
        'm': m,
    }
    return render(request, "estaciones/estaciones.html", context)

def estacion(request):
    return render(request, "estaciones/estacion.html")