from enum import unique
from pyexpat import model
from django.db import models
from django.utils.translation import gettext as _

from apps.Usuarios.models import Usuario

# Create your models here.

def estacion_directory_path(instance, filename):
    return 'estacion_{0}/{1}'.format(instance.codigo, filename)
    
class Estacion(models.Model):

    class FormatoChoices(models.TextChoices):
        DEG_MIN_SEC = 'DMS', _('Degrees Minutes Seconds')
        DEG_DEC = 'DD', _('Degrees Decimal')

    codigo = models.CharField(_("codigo"), max_length=255)
    nombre = models.CharField(_("nombre"), max_length=255)
    tipo = models.CharField(_("tipo"), max_length=255)
    provincia = models.CharField(_("provincia"), max_length=255)
    estado = models.CharField(_("estado"), max_length=255)
    fecha_instalacion = models.DateField(_("fecha_instalacion"))
    latitud = models.CharField(_("latitud"), max_length=50)
    longitud = models.CharField(_("longitud"), max_length=50)
    formato = models.CharField(_("formato"), max_length=50, choices=FormatoChoices.choices, default=FormatoChoices.DEG_MIN_SEC)
    archivo_csv = models.FileField(_("archivo_csv"), upload_to=estacion_directory_path)

    class Meta:
        verbose_name='estacion'
        verbose_name_plural='estaciones'

    def __str__(self):
        return "{0} : {1}".format(self.codigo, self.nombre)

class EstacionSuscripcion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)

    class Meta:
        verbose_name='suscripcion'
        verbose_name_plural='suscripciones'
        unique_together = (("usuario", "estacion"),)

    def __str__(self):
        return "{0} : {1}".format(self.usuario.email, self.estacion.nombre)
