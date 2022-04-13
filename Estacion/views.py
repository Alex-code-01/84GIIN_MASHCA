from django.shortcuts import render

import folium
from Estacion.models import Estacion
from Estacion.modules import estacion_funciones as ef

# Create your views here.

def estaciones(request):  
    Ecuador = [-1.4526567126141714, -78.41862277481742]  
    m = folium.Map(location=Ecuador, zoom_start=6.5)
    for e in Estacion.objects.raw('SELECT * FROM Estacion_estacion'):
        #Degree, Minutes, Seconds        
        if e.formato==Estacion.FormatoChoices.DEG_MIN_SEC:
            lat = ef.conv_DMS_a_DD(e.latitud)
            long = ef.conv_DMS_a_DD(e.longitud)
        #Degree Decimal        
        elif e.formato==Estacion.FormatoChoices.DEG_DEC:
            lat = float(e.latitud)
            long = float(e.longitud)    
        html="<b>Estación:</b><br><a href=estacion/{0} target=_top class=linksEstaciones>{1}</a><br>{0}".format(e.codigo, e.nombre)        
        #popup="<b>Estación: </b><br><a href=\"{{ url 'Estacion' {0} }}\" target=_top class=linksEstaciones>{1}</a><br>{0}".format(e.codigo, e.nombre)        
        folium.Marker(
            [lat, long], 
            tooltip='Selecciona para visualizar', 
            popup=folium.Popup(html),            
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

def historico(request, codigo):   
    estacion = Estacion.objects.get(codigo=codigo)
    context={
        "estacion": estacion
    } 
    return render(request, "estaciones/historico.html", context)

def prediccion(request, codigo):   
    estacion = Estacion.objects.get(codigo=codigo)
    context={
        "estacion": estacion
    } 
    return render(request, "estaciones/prediccion.html", context)
