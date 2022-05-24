from multiprocessing import context
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "WebApp/home.html")

def contacto(request):
    return render(request, "WebApp/contacto.html")
