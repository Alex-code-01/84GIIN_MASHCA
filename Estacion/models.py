from pyexpat import model
from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
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

    class Meta:
        verbose_name='estacion'
        verbose_name_plural='estaciones'

    def __str__(self):
        return "{0} : {1}".format(self.codigo, self.nombre)

class DatosCalamaca(models.Model):
    fecha = models.DateTimeField(_("Fecha"))
    temp_media = models.FloatField(_("Temperatura"))
    temp_max = models.FloatField(_("TMax"))
    temp_min = models.FloatField(_("TMin"))
    humedad = models.FloatField(_("Humedad"))
    h_r_max = models.FloatField(_("H_R Max"))
    h_m_min = models.FloatField(_("H_M Min"))
    precipitacion = models.FloatField(_("Precipitacion"))
    direccion = models.FloatField(_("Direccion"))
    velocidad = models.FloatField(_("Velocidad"))
