from codecs import strict_errors
import unittest
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
        parameter = request.GET.get('select', parameters_list[0]) #se obtiene el resultado del objeto select (por defecto se selecciona el primer parametro)
        
        data_selected = select_data(data, parameter, desde, hasta)

        date_list = list(data_selected.iloc[:, 0])
        values_list = list(data_selected.iloc[:, 1])
        values_list = convert_data(values_list, float)
        print(data_selected)

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

def select_data(data, parameter, since, until):
    date_list = []
    parameter_list = []
    since = str_to_date(since, '%Y-%m-%d')
    until = str_to_date(until, '%Y-%m-%d')
    
    data = data[[data.columns[0], parameter]]

    for item in range(len(data)):
        date = data[data.columns[0]][item]
        date = str_to_date(date, '%d/%m/%Y %H:%M:%S')
        if date > since and date < until:
            date_list.append(date_to_str(date, '%d/%m/%Y %H:%M:%S'))
            parameter_list.append(data[parameter][item])
    
    result = {data.columns[0]: date_list, parameter: parameter_list}
    df = pd.DataFrame(result)    
    return df

def convert_data(data, type):    
    result = []
    if type == float:        
        for item in data:
            item = item.replace(",", ".")
            result.append(float(item))
    return result

def str_to_date(date, format):
    return datetime.strptime(date, format)

def date_to_str(date, format):
    return date.strftime(format)



    
