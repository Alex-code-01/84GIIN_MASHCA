from django.shortcuts import render, HttpResponse

# Create your views here.

def home(request):
    return render(request, "WebApp/home.html")

def estaciones(request):
    return render(request, "WebApp/estaciones.html")

def contacto(request):
    return render(request, "WebApp/contacto.html")

def login(request):
    return render(request, "WebApp/login.html")