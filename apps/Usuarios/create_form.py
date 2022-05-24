from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class CreateUser(UserCreationForm):    
    class Meta:
        model=Usuario
        fields=['username', 'email', 'password1', 'password2']