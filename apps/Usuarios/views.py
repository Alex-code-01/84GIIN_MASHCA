from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
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
        form = UserCreationForm()
        if form.is_valid():            
            user=form.save()
            login(request, user)                         
    else:
        form = UserCreationForm()

    context = {
        "form": form
    }
    return render(request, "usuarios/agregar_usuario.html", context)    

def modificar_usuario(request):    
    return render(request, "usuarios/modificar_usuario.html")    

def eliminar_usuario(request):
    return render(request, "usuarios/eliminar_usuario.html")    

def login_view(request):
    if request.method=='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():            
            user=form.get_user()
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
