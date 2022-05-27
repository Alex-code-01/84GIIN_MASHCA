from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class ConfigDate(models.Model):
    class UnitChoices(models.TextChoices):
        dias = 'dias',
        meses = 'meses',
        semanas = 'semanas',
        annos = 'annos'

    parameter = models.CharField(_("parametro"), max_length=255) 
    value = models.CharField(_("valor"), max_length=255) 
    unit = models.CharField(_("unidad"), max_length=255, choices=UnitChoices.choices, default=UnitChoices.dias)

    class Meta:
        verbose_name='configuracion_fecha'
        verbose_name_plural='configuraciones_Fechas'

    def __str__(self) -> str:
        return "{}: {} {}".format(self.parameter, self.value, self.unit)