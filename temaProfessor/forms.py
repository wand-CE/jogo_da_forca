from django import forms
from django.forms import inlineformset_factory

from temaProfessor.models import Palavra, Tema


class PalavraForm(forms.ModelForm):
    class Meta:
        model = Palavra
        fields = ['palavra']


PalavraFormSet = inlineformset_factory(Tema, Palavra, form=PalavraForm, extra=1, can_delete=True)
