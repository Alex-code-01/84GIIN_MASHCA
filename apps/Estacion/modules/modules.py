import os
import pandas as pd
import folium
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apps.WebApp.models import ConfigDate
from apps.Estacion.models import Estacion

def represent_map(pais, zoom):
    return folium.Map(location=pais, zoom_start=zoom)    

def locate_estaciones(map, estaciones):
    for e in estaciones:               
        if e.formato==Estacion.FormatoChoices.DEG_MIN_SEC:
            coordinates = [conv_DMS_a_DD(e.latitud), conv_DMS_a_DD(e.longitud)]                    
        elif e.formato==Estacion.FormatoChoices.DEG_DEC:
            coordinates = [float(e.latitud), float(e.longitud)]
        html="<b>Estación:</b><br><a href=estacion/{0} target=_top class=linksEstaciones>{1}</a><br>{0}".format(e.codigo, e.nombre)         
        folium.Marker(
            coordinates, 
            tooltip='Selecciona para visualizar', 
            popup=folium.Popup(html),            
            icon=folium.Icon(icon="cloud"),          
        ).add_to(map)
    return map

def read_csv_file(nombre_archivo):    
    global my_file
    archivo = os.path.join(os.getcwd(), "media", str(nombre_archivo))
    my_file = pd.read_csv(archivo)    
    return pd.DataFrame(data=my_file, index=None)

def select_data(data, parameter, since, until):
    date_list, parameter_list = [], []     
    since, until = str_to_date(since, '%Y-%m-%d'), str_to_date(until, '%Y-%m-%d')    
    data = data[[data.columns[0], parameter]]
    for item in range(len(data)):        
        date = str_to_date(data[data.columns[0]][item], '%d/%m/%Y %H:%M:%S')
        if date > since and date < until:
            date_list.append(date_to_str(date, '%d/%m/%Y %H:%M:%S'))
            parameter_list.append(data[parameter][item])
    return date_list, parameter_list

def convert_data(data, type):    
    result = []
    if type == float:        
        result = [float(item.replace(",",".")) for item in data]
    return result

def str_to_date(date, format):
    return datetime.strptime(date, format)

def date_to_str(date, format):
    return date.strftime(format)

def date_today():
    return datetime.today()

def add_time(from_date, value, unit):
    if unit == ConfigDate.UnitChoices.dias.lower():
        date = from_date + relativedelta(days=value)
    elif unit == ConfigDate.UnitChoices.semanas.lower():
        date = from_date + relativedelta(weeks=value)
    elif unit == ConfigDate.UnitChoices.meses.lower():
        date = from_date + relativedelta(months=value)
    elif unit == ConfigDate.UnitChoices.annos.lower():
        date = from_date + relativedelta(years=value)
    else:
        date = None
    return date

def conv_DMS_a_DD(param):
    deg, minutes, seconds, direction = param[:2], param[2:4], param[4:6], param[6]
    return (float(deg)+ float(minutes)/60 + float(seconds)/(60*60))*(-1 if direction in ['W', 'S'] else 1)    
