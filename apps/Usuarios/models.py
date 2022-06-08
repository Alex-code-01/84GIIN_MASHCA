from django.db import models
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

def usuario_directory_path(instance, filename):
    return 'usuario_{0}/{1}'.format(instance.username, filename)

class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    rol = models.CharField('Rol', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.rol
    
    def save(self, *args, **kwargs):
        permisos = ['add', 'change', 'delete', 'view']
        if not self.id:
            nuevo_grupo, creado = Group.objects.get_or_create(name=f'{self.rol}')
            for permiso_tmp in permisos:
                permiso,created=Permission.objects.update_or_create(
                    name = f'Can {permiso_tmp} {self.rol}',
                    content_type = ContentType.objects.get_for_model(Rol),
                    codename = f'{permiso_tmp}_{self.rol}'
                )
                if creado:
                    nuevo_grupo.permissions.add(permiso.id)
            super().save(*args, **kwargs) 
        else:
            rol_antiguo = Rol.objects.filter(id=self.id).values('rol').first()
            if rol_antiguo['rol'] == self.rol:
                super().save(*args, **kwargs)
            else:
                Group.objects.filter(name=rol_antiguo['rol']).update(name=f'{self.rol}')
                for permiso_tmp in permisos:
                    Permission.objects.filter(codename=f"{permiso_tmp}_{rol_antiguo['rol']}").update(
                        codename = f'{permiso_tmp}_{self.rol}',
                        name = f'Can {permiso_tmp} {self.rol}'
                    )
                super().save(*args, **kwargs)

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, nombres, password):
        if not email:
            raise ValueError('El usuario debe tener correo electrónico')
        usuario = self.model(
            username = username,
            email = self.normalize_email(email),
            nombres = nombres            
        )
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, email, username, nombres, password):        
        usuario = self.create_user(
            username = username,
            email = self.normalize_email(email),
            nombres = nombres,           
            password = password
        )
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nombre de usuario', unique=True, max_length=100)    
    email = models.EmailField('Correo Electrónico', unique=True, max_length=254)
    nombres = models.CharField('Nombre(s)', max_length=200, blank=True, null=True)
    apellidos = models.CharField('Apellidos', max_length=200, blank=True, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, blank=True, null=True)
    imagen = models.ImageField('Imagen de perfil', upload_to=usuario_directory_path, blank=True, null=True)
    is_active = models.BooleanField('Activo', default=True)
    is_staff = models.BooleanField('Miembro', default=False)
    is_superuser = models.BooleanField('Superusuario', default=False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombres']
    
    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"

