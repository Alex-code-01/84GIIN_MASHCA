from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from WebApp.models import Config
from Estacion.models import Estacion
from Estacion.modules import modules as mod

# Create your views here.

@login_required
def estaciones(request):  
    Ecuador = [-1.4526567126141714, -78.41862277481742]      
    estaciones = Estacion.objects.raw('SELECT * FROM Estacion_estacion')
    map = mod.represent_map(Ecuador, 6.5)    
    map = mod.locate_estaciones(map, estaciones)    
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
    parameter, since, until, min_date, max_date = None, None, None, None, None

    if request.user.has_perm('view_Administrador') or request.user.has_perm('view_EnteGubernamental'):        
        min_date=None
    else:
        min_time_value = int(Config.objects.get(parameter="historico_min_date").value)
        min_time_unit =  Config.objects.get(parameter="historico_min_date").unit.lower()
        min_date = mod.date_to_str(mod.add_time(mod.date_today(), -min_time_value, min_time_unit), '%Y-%m-%d')
        
    max_time_value = int(Config.objects.get(parameter="historico_max_date").value)
    max_time_unit =  Config.objects.get(parameter="historico_max_date").unit.lower()
    max_date = mod.date_to_str(mod.add_time(mod.date_today(), max_time_value, max_time_unit), '%Y-%m-%d')
    if estacion.archivo_csv:                                          
        data = mod.read_csv_file(estacion.archivo_csv)
        parameters_list = list(data.columns[1:])
                
        since = request.GET.get('since', mod.date_to_str(mod.date_today(), '%Y-%m-%d'))        
        until = request.GET.get('until', mod.date_to_str(mod.date_today(), '%Y-%m-%d'))                                 
        parameter = request.GET.get('param', parameters_list[0])
        
        data_selected = mod.select_data(data, parameter, since, until)
        date_list, values_list = data_selected[0], mod.convert_data(data_selected[1], float)        
    else: 
        print("No hay datos históricos de la estación")
    context={
        "estacion": estacion,
        "date_list": date_list,
        "values_list": values_list,
        "parameters_list": parameters_list,
        "selected": parameter,
        "since": since,
        "until": until,
        "min_date": min_date,
        "max_date": max_date,
    } 
    return render(request, "estaciones/historico.html", context)

def prediccion(request, codigo):         
    estacion = Estacion.objects.get(codigo=codigo)
    context={
        "estacion": estacion,       
    } 
    return render(request, "estaciones/prediccion.html", context)
    