from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .create_form import CreateUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuario

# Create your views here.

def usuarios(request): 
    usuarios = Usuario.objects.all()    
    context = {
        "users": usuarios        
    }   
    return render(request, "usuarios/usuarios.html", context)

def agregar_usuario(request):
    if request.method=='POST':        
        form = CreateUser(request.POST)
        if form.is_valid():            
            form.save()
            return redirect('Usuarios')                        
    else:
        form = CreateUser()

    context = {
        "form": form
    }
    return render(request, "usuarios/agregar_usuario.html", context)    

def modificar_usuario(request):  
    
    return render(request, "usuarios/modificar_usuario.html")    

def eliminar_usuario(request, username):
    try:
        user = Usuario.objects.get(username=username)
        user.delete()
        messages.success(request, "El usuario ha sido eliminado")
        return redirect('Usuarios')
    except:
        messages.error(request, "El usuario no ha sido encontrado")
        return render(request, "usuarios/eliminar_usuario.html")    

def login_view(request):
    if request.method=='POST':
        form = AuthenticationForm(request, data=request.POST)
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
             

    form = AuthenticationForm()
    return render(request, "usuarios/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('Home')
