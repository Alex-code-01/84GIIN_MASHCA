# 84GIIN_MASHCA

## Grado en Ingeniería Informática - 84GIIN Trabajo Fin de Grado
#### Tutor: Roger Clotet Martínez

## Herramientas

- Django: pip install django
- Python venv: pip install virtualenv
- Folium: pip install folium
- ChartJS: pip install django-chartjs
- Bootstrap: pip install django-bootstrap-v5
- MySQL: pip install mysqlclient
- Visual Studio Code
- Git

## Comandos
#### Para activar el entorno virtual:
```
pip install -r requirements.txt
```
#### Para activar el entorno virtual:
```
venv\Scripts\activate
```

#### Para ejecutar el proyecto: 
```
python manage.py runserver
```

#### Para ejecutar las migraciones de los modelos y la Base de Datos: 
```
python manage.py makemigrations
python manage.py migrate
```

#### Para migrar de Base de Datos:
```
./manage.py dumpdata --output data.json
```
- Se abre el archivo JSON y se guarda con encodding UTF-8
- Se modifica la configuración de la Base de Datos en settings.py
```
python manage.py migrate
./manage.py loaddata data.json
```
