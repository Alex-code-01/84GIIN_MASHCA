from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from Estacion.models import Estacion
from Estacion.modules import estacion_funciones as est_func

# Create your views here.

@login_required
def estaciones(request):  
    Ecuador = [-1.4526567126141714, -78.41862277481742]      
    estaciones = Estacion.objects.raw('SELECT * FROM Estacion_estacion')
    map = est_func.represent_map(Ecuador, 6.5)    
    map = est_func.locate_estaciones(map, estaciones)    
    map = map._repr_html_()
    context = {
        'map': map,
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
    date_list,  values_list, parameters_list  = [], [], []     
    parameter, since, until = None, None, None   
    if estacion.archivo_csv:                                          
        data = est_func.read_csv_file(estacion.archivo_csv)
        parameters_list = list(data.columns[1:])
        
        since = request.GET.get('desde', est_func.date_to_str(est_func.date_today(), '%Y-%m-%d'))        
        until = request.GET.get('hasta', est_func.date_to_str(est_func.date_today(), '%Y-%m-%d'))                                 
        parameter = request.GET.get('param', parameters_list[0])
        
        data_selected = est_func.select_data(data, parameter, since, until)
        date_list, values_list = data_selected[0], est_func.convert_data(data_selected[1], float)        
    else: 
        print("No hay datos históricos de la estación")
    context={
        "estacion": estacion,
        "date_list": date_list,
        "values_list": values_list,
        "parameters_list": parameters_list,
        "selected": parameter,
        "desde": since,
        "hasta": until,
    } 
    return render(request, "estaciones/historico.html", context)

def prediccion(request, codigo):   
    estacion = Estacion.objects.get(codigo=codigo)
    context={
        "estacion": estacion
    } 
    return render(request, "estaciones/prediccion.html", context)
    