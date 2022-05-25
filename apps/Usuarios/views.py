from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .create_form import UserForm, LoginUser, ModifyUser
from .models import Usuario

# Create your views here.
@staff_member_required
def usuarios(request): 
    usuarios = Usuario.objects.all()    
    context = {
        "users": usuarios        
    }   
    return render(request, "usuarios/usuarios.html", context)

@staff_member_required
def agregar_usuario(request):
    if request.method=='POST':        
        form = UserForm(request.POST)           
        if form.is_valid():            
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"El usuario {username} ha sido agregado correctamente")
            return redirect('Usuarios')                        
    else:
        form = UserForm()

    context = {
        "title": "Agregar Usuario", 
        "form": form
    }
    return render(request, "usuarios/formulario_usuario.html", context)    

@staff_member_required
def modificar_usuario(request, userid): 
    context = {}
    try:
        user = Usuario.objects.get(id=userid) 
        form = ModifyUser(instance=user)                            
        context['title'] = "Modificar Usuario"
        context['form'] = form
        if request.method == 'POST':
            form = ModifyUser(data=request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, f"El usuario {user.username} ha sido modificado correctamente")
                return redirect('Usuarios')        
    except:
        messages.error(request, "El usuario no ha sido encontrado")
        return redirect('Usuarios')        
    return render(request, "usuarios/formulario_usuario.html", context)     

@staff_member_required
def eliminar_usuario(request, userid):
    try:
        user = Usuario.objects.get(id=userid)
        user.delete()
        messages.success(request, f"El usuario {user.username} ha sido eliminado correctamente")
        return redirect('Usuarios')
    except:
        messages.error(request, "El usuario no ha sido encontrado")
        return redirect('Usuarios')

def login_view(request):
    if request.method=='POST':
        form = LoginUser(request, data=request.POST)
        if form.is_valid():                        
            user_name = form.cleaned_data.get("username")
            passwd = form.cleaned_data.get("password")
            user = authenticate(username=user_name, password=passwd)
            if user is not None:                
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next')) 
                else:
                    return redirect('Home')             
        else:
            messages.error(request, "Usuario y/o contraseña incorrectos")              
    form = LoginUser()
    return render(request, "usuarios/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('Home')
