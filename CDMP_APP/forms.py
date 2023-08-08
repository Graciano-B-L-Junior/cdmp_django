from django import forms

class GastoForm(forms.Form):
    valor = forms.FloatField()
    descricao = forms.CharField(max_length=50)
    data_gasto = forms.DateField()
    categoria = forms.CharField()