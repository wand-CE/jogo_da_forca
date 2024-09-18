from django import forms


class LetraForm(forms.Form):
    letra = forms.CharField(max_length=1, required=True, label='Digite uma letra')
