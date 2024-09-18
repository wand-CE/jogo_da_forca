from django.contrib.auth.models import User
from django import forms


class UsuarioForm(forms.ModelForm):
    TIPO_USUARIO_CHOICES = [
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
    ]

    tipo_usuario = forms.TypedChoiceField(choices=TIPO_USUARIO_CHOICES, coerce=str, label='Tipo de usuário')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
