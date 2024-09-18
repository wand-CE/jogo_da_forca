from django import forms
from django.utils import timezone

from temaProfessor.models import Tema


class LetraForm(forms.Form):
    letra = forms.CharField(max_length=1, required=True, label='Digite uma letra')


class RelatorioFiltroForm(forms.Form):
    tema = forms.ModelChoiceField(queryset=Tema.objects.all(), required=False)
    data_inicio = forms.DateField(required=False, widget=forms.SelectDateWidget)
    data_fim = forms.DateField(required=False, widget=forms.SelectDateWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_inicio'].initial = timezone.now().date()
        self.fields['data_fim'].initial = timezone.now().date()
