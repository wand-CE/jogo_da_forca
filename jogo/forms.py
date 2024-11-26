from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

from temaProfessor.models import Tema


class LetraForm(forms.Form):
    letra = forms.CharField(max_length=1, required=True, label='Digite uma letra')


class RelatorioFiltroForm(forms.Form):
    tema = forms.ModelChoiceField(queryset=Tema.objects.all(), required=False)
    data_inicio = forms.DateField(required=False, widget=forms.SelectDateWidget)
    data_fim = forms.DateField(required=False, widget=forms.SelectDateWidget)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['tema'].queryset = Tema.objects.filter(criado_por=user)
        self.fields['data_inicio'].initial = timezone.now().date()
        self.fields['data_fim'].initial = timezone.now().date()
