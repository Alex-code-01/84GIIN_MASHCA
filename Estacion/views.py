from django.shortcuts import render

import folium
from Estacion.models import Estacion
from Estacion.modules import estacion_funciones as ef
# Create your views here.

def estaciones(request):    
    m = folium.Map(location=[-1.671743709620801, -78.660423157757], zoom_start=6.5)
    for e in Estacion.objects.raw('SELECT * FROM Estacion_estacion'):
        #degree, minutes, seconds
        if e.formato=="dms":
            lat = ef.conv_DMS_a_DD(e.latitud)
            long = ef.conv_DMS_a_DD(e.longitud)
        #degree decimal
        elif e.formato=="dd": 
            lat = e.latitud
            long = e.longitud
        popup="<b>Estación: </b><br><a href="+"estacion/"+str(e.codigo)+" target=_top class=linksEstaciones>" + e.nombre + "</a><br>" + e.codigo
        folium.Marker(
            [lat, long], 
            tooltip='Selecciona para visualizar', 
            popup=folium.Popup(popup),            
            icon=folium.Icon(icon="cloud"),          
        ).add_to(m) 

    m = m._repr_html_()
    context = {
        'm': m,
    }
    return render(request, "estaciones/estaciones.html", context)

def estacion(request, codigo):
    estacion = Estacion.objects.get(codigo=codigo)
    context={
        "estacion": estacion
    }
    return render(request, "estaciones/estacion.html", context)