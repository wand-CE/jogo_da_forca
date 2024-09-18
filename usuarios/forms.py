from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class UsuarioForm(forms.ModelForm):
    TIPO_USUARIO_CHOICES = [
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
    ]

    tipo_usuario = forms.TypedChoiceField(choices=TIPO_USUARIO_CHOICES, coerce=str, label='Tipo de usuário')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirme a Senha')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'tipo_usuario')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise ValidationError("As senhas não coincidem")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user
