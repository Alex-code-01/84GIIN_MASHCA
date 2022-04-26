from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import os
import pandas as pd
import folium
from datetime import date, datetime
from Estacion.models import Estacion
from Estacion.modules import estacion_funciones as ef

# Create your views here.

@login_required
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
    date_list = []
    values_list = []
    parameters_list = []  
    parameter = None
    desde = None
    hasta = None
    if estacion.archivo_csv:                                          
        data = leer_archivo_csv(estacion.archivo_csv) #datos del CSV
        parameters_list = list(data.columns[1:]) #lista de los parametros        
        desde = request.GET.get('desde', str(datetime.today().strftime('%Y-%m-%d')))        
        hasta = request.GET.get('hasta', str(datetime.today().strftime('%Y-%m-%d')))                         
        date_list = lista_fechas(desde, hasta, list(data['Fecha']))               
        parameter = request.GET.get('select', parameters_list[0]) #se obtiene el resultado del objeto select (por defecto se selecciona el primer parametro)
        values_list = seleccionar_data(data, parameter, float) #se obtienen los datos requeridos             

    else: 
        print("No hay datos históricos de la estación")
    context={
        "estacion": estacion,
        "date_list": date_list,
        "values_list": values_list,
        "parameters_list": parameters_list,
        "selected": parameter,
        "desde": desde,
        "hasta": hasta,
    } 
    return render(request, "estaciones/historico.html", context)

def prediccion(request, codigo):   
    estacion = Estacion.objects.get(codigo=codigo)
    context={
        "estacion": estacion
    } 
    return render(request, "estaciones/prediccion.html", context)

def leer_archivo_csv(nombre_archivo):    
    global rows, columns, data, missing_values, my_file
    
    current_dir = os.getcwd()
    nombre_archivo = "{0}{1}{2}".format(current_dir, '\media\\', nombre_archivo)    
    
    my_file = pd.read_csv(nombre_archivo)
        
    data = pd.DataFrame(data=my_file, index=None)

    rows = len(data.axes[0])
    columns = len(data.axes[1])

    null_data = data[data.isnull().any(axis=1)]
    missing_values = len(null_data)
    
    return data

def seleccionar_data(data, values, type):
    values_list = []
    list_values = list(data[values])
    if type == float:        
        for item in list_values:
            item = item.replace(",", ".")
            values_list.append(float(item))
    return values_list

def lista_fechas(desde, hasta, fechas):
    fechas_select = []
    desde = datetime.strptime(desde, '%Y-%m-%d')
    hasta = datetime.strptime(hasta, '%Y-%m-%d')
    for fecha in fechas:     
        fecha = datetime.strptime(fecha, '%d/%m/%Y %H:%M:%S')   
        if fecha > desde and fecha < hasta:
            fechas_select.append(fecha.strftime('%d/%m/%Y %H:%M:%S'))
    return fechas_select