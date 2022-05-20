from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class Config(models.Model):
    class UnitChoices(models.TextChoices):
        dias = 'dias',
        meses = 'meses',
        semanas = 'semanas',
        annos = 'annos'

    parameter = models.CharField(_("parametro"), max_length=255) 
    value = models.CharField(_("valor"), max_length=255) 
    unit = models.CharField(_("unidad"), max_length=255, choices=UnitChoices.choices, default=UnitChoices.dias)

    def __str__(self) -> str:
        return "{}: {} {}".format(self.parameter, self.value, self.unit)