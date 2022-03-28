from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class Estacion(models.Model):
    codigo = models.CharField(_("codigo"), max_length=255)
    nombre = models.CharField(_("nombre"), max_length=255)
    tipo = models.CharField(_("tipo"), max_length=255)
    provincia = models.CharField(_("provincia"), max_length=255)
    estado = models.CharField(_("estado"), max_length=255)
    fecha_instalacion = models.DateField(_("fecha_instalacion"))
    latitud = models.CharField(_("latitud"), max_length=50)
    longitud = models.CharField(_("longitud"), max_length=50)

    def __str__(self):
        return "{0} : {1}".format(self.codigo, self.nombre)
