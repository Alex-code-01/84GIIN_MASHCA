# 84GIIN_MASHCA

## Grado en Ingeniería Informática - 84GIIN Trabajo Fin de Grado
#### Tutor: Roger Clotet Martínez

## Herramientas

- Django: pip install django
- Folium: pip install folium
- Bootstrap
- MySQL
- Visual Studio Code
- Git

## Comandos

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
