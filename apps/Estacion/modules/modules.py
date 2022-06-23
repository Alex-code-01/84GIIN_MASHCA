import os
import pandas as pd
import folium
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apps.WebApp.models import ConfigDate
from apps.Estacion.models import Estacion
from apps.WebApp.modules.config_modules import queryConfig
from django.core.exceptions import ObjectDoesNotExist

def represent_map(pais, zoom):
    """
    Returns a map located in the country and with the zoom specified
    Atributes:
        pais -> String specifying the country in wich the map is located initially
        zoom -> Float value that specifies the zoom in or zoom out
    """
    return folium.Map(location=pais, zoom_start=zoom)    

def locate_estaciones(map, estaciones):
    """
    Returns a map locating all the estations specified
    Atributes:
        map -> Map represented in the HTML file
        estaciones -> QuerySet of the stations stored in the DataBase
    """
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
    """
    Returns a DataFrame of the CSV specified
    Atributes:
        nombre_archivo -> Name of the CSV file containing the data
    """  
    global my_file
    archivo = os.path.join(os.getcwd(), "media", str(nombre_archivo))
    my_file = pd.read_csv(archivo)    
    return pd.DataFrame(data=my_file, index=None)

def select_data(data, parameter, since, until):
    """
    Returns two lists containing the timeline (date_list) and the data (parameter_list) between the dates specified
    Atributes:
        data -> data to select from
        parameter -> parameter to select from the data (Example: "Temperature")
        since -> Date object that specifies the value from which the data is selected
        until -> Date object that specifies the value up to which data is selected
    """
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
    """
    Returns the data converted to the required type
    Atributes:
        data -> List object containing the data
        type -> Type to convert the data to (Example: float)
    """   
    result = []
    if type == float:        
        result = [float(item.replace(",",".")) for item in data]
    return result

def str_to_date(date, format):
    """
    Returns Date object of a String object
    Atributes:
        date -> String object to convert
        format -> Format to convert the string to Date (Example: '%Y-%m-%d')
    """
    return datetime.strptime(date, format)

def date_to_str(date, format):
    """
    Returns String object of a Date object
    Atributes:
        date -> Date object to convert
        format -> Format to convert the date to the string (Example: '%Y-%m-%d')
    """
    return date.strftime(format)

def date_today():
    """
    Returns the current date
    """
    return datetime.today()

def add_time(from_date, value, unit):
    """
    Returns the result of adding a certain date another time value
    Atributes:
        from_date -> starting date on which to operate
        value -> number of units to add to from_date
        unit -> unit of time (days, weeks, months, years)
    """
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

def get_date(parameter, operation):
    """
    Returns the date result of applying the limitation of the parameter    
    Atributes:
        parameter -> specified instance of configuration table
        operation -> "add" for adding or "rest" for subtracting the date limit
    """
    try:
        time = queryConfig(parameter)
        if operation == "rest":
            time[0] = -time[0]
        return date_to_str(add_time(date_today(), time[0], time[1]), '%Y-%m-%d')       
    except ObjectDoesNotExist:
        return None

def conv_DMS_a_DD(param):
    """
    Returns a Degrees Decimal (DD) value from an Degrees Minutes and Seconds (DMS) value 
    Atributes:
        param -> Degrees Minutes and Seconds value to convert
    """
    deg, minutes, seconds, direction = param[:2], param[2:4], param[4:6], param[6]
    return (float(deg)+ float(minutes)/60 + float(seconds)/(60*60))*(-1 if direction in ['W', 'S'] else 1)    
