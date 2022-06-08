from django.contrib import messages
from django.shortcuts import render
from .models import ContactForm

# Create your views here.

def home(request):
    return render(request, "WebApp/home.html")

def contacto(request):
    if request.method=='POST':
        nombre = request.POST.get("name")
        email = request.POST.get("email")
        mensaje = request.POST.get("message")
        contact_msg = ContactForm(name=nombre, email=email, message=mensaje)
        contact_msg.save()
        messages.success(request, f"El formulario ha sido enviado correctamente")
    return render(request, "WebApp/contacto.html")
