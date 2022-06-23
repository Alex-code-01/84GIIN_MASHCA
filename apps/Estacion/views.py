from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Estacion, EstacionSuscripcion
from .modules import modules as mod

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
    suscriptions = EstacionSuscripcion.objects.all()
    user, suscribed, suscribe_butt = request.user, False, "Suscribir"         
    for sus in suscriptions:
        if sus.usuario == user and sus.estacion == estacion:
            suscribed = True
            suscribe_butt = "Cancelar suscripción"
    try: 
        if request.method == 'POST':            
            if not suscribed:                        
                suscription = EstacionSuscripcion(usuario=user, estacion=estacion)                                       
                suscription.save()                  
                messages.success(request, f"Se ha suscrito a la estación")
                return redirect('Estacion', estacion.codigo)
            else:
                suscription  = EstacionSuscripcion.objects.get(usuario=user, estacion=estacion)
                suscription.delete()
                messages.success(request, f"Se ha desuscrito de la estación")
                return redirect('Estacion', estacion.codigo)
    except IntegrityError:
        messages.warning(request, f"Ya está suscrito a la estación")        
        
    context={
        "estacion": estacion,
        "sus_butt_text": suscribe_butt
    }
    return render(request, "estaciones/estacion.html", context)

def historico(request, codigo):   
    estacion = Estacion.objects.get(codigo=codigo)  
    date_list,  values_list, parameters_list  = [], [], []
    parameter, since, until, min_date, max_date = None, None, None, None, None

    if request.user.has_perm('view_Administrador') or request.user.has_perm('view_EnteGubernamental'):        
        min_date=None
    else:
        min_date = mod.get_date("historico_min_date", "rest")

    max_date = mod.get_date("historico_max_date", "add")
    
    date_value = mod.date_to_str(mod.date_today(), '%Y-%m-%d')

    if estacion.archivo_csv:                                          
        data = mod.read_csv_file(estacion.archivo_csv)
        parameters_list = list(data.columns[1:])
        if request.method == 'GET':                
            since = request.GET.get('since', date_value)        
            until = request.GET.get('until', date_value)                                 
            parameter = request.GET.get('param', parameters_list[0])
            
            data_selected = mod.select_data(data, parameter, since, until)
            date_list, values_list = data_selected[0], mod.convert_data(data_selected[1], float)                            
    context={
        "estacion": estacion,        
        "parameters_list": parameters_list,        
        "since": since,
        "until": until,
        "min_date": min_date,
        "max_date": max_date,
        'date_list': date_list,
        'values_list': values_list,
        'selected': parameter,
    } 
    return render(request, "estaciones/historico.html", context)

def prediccion(request, codigo):         
    estacion = Estacion.objects.get(codigo=codigo)        
    context={
        "estacion": estacion,       
    } 
    return render(request, "estaciones/prediccion.html", context)
    