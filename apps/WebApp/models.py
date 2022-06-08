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
        verbose_name='Configuracion_Fecha'
        verbose_name_plural='Configuraciones_Fechas'

    def __str__(self) -> str:
        return f"{self.parameter}: {self.value} {self.unit}"        

class ContactForm(models.Model):
    name = models.CharField("Nombre", max_length=255) 
    email = models.EmailField('Correo Electrónico', max_length=255)
    message = models.CharField("Mensaje", max_length=500)

    class Meta:
        verbose_name='Contacto_Mensaje'
        verbose_name_plural='Contacto_Mensajes'
    
    def __str__(self) -> str:
        return f"{self.email}: {self.message}"
