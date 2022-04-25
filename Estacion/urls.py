from django.urls import path

from . import views

urlpatterns = [
    path('', views.estaciones, name="Estaciones"),
    path('estacion/<str:codigo>', views.estacion, name="Estacion"),    
    path('estacion/<str:codigo>/historico/', views.historico, name="Historico"),        
    path('estacion/<str:codigo>/prediccion', views.prediccion, name="Prediccion"),
]