from email import message
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def usuarios(request):    
    return render(request, "usuarios/usuarios.html")

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
