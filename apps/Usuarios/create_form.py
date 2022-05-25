from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.forms import PasswordInput
from .models import Usuario

class UserForm(UserCreationForm):    
    class Meta:
        model=Usuario
        fields=['username', 'password1', 'password2', 'email', 'nombres', 'apellidos', 'rol', 'is_active', 'is_superuser']

class ModifyUser(UserChangeForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model=Usuario
        fields=['username', 'password', 'email', 'nombres', 'apellidos', 'rol', 'is_active', 'is_superuser']

class LoginUser(AuthenticationForm):
    class Meta:
        model=Usuario
        fields=['username', 'password1']