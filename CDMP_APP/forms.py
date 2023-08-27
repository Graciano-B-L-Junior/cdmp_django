from django import forms
from datetime import datetime
from .models import Categoria,Depositos,MetaFinanceira

def set_choices_categoria() -> tuple:
        categorias = Categoria.objects.all()
        tupla= tuple()
        lista=[]
        for categoria in categorias:
              lista.append(categoria.nome)
        tupla = ((categoria,categoria) for categoria in lista)
        return tupla
class DespesaForm(forms.Form):
    valor = forms.FloatField(error_messages={"invalid":"Preencha o campo apenas com números"})
    descricao = forms.CharField(max_length=50)
    data_gasto = forms.DateField(widget=forms.DateInput(attrs={'type':'date','max':datetime.now().date}))
    categoria = forms.ChoiceField(widget=forms.Select,choices=set_choices_categoria())

class DepositoForm(forms.ModelForm):
      class Meta:
            model = Depositos
            fields = ["valor","descricao","data_deposito"]
            widgets ={
                  "data_deposito":forms.DateInput(attrs={'type':'date','max':datetime.now().date})
            }

class MetaFinanceiraForm(forms.ModelForm):
      class Meta:
            model = MetaFinanceira
            fields = ["nome_meta","valor_atual","valor_total"]
            widgets = {
                  "valor_atual":forms.NumberInput(),
                  "valor_total":forms.NumberInput()
            }

    
