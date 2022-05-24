from django.urls import path

from . import views

urlpatterns = [
    path('', views.usuarios, name="Usuarios"),    
    path('agregar_usuario/', views.agregar_usuario, name="AgregarUsuario"), 
    path('modificar_usuario/', views.modificar_usuario, name="ModificarUsuario"), 
    path('eliminar_usuario/<str:username>', views.eliminar_usuario, name="EliminarUsuario"), 
    path('login/', views.login_view, name="Login"),    
    path('logout/', views.logout_view, name="Logout"), 
]