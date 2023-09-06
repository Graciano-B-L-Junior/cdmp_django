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
    data_despesa = forms.DateField(widget=forms.DateInput(attrs={'type':'date','max':datetime.now().date}))
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
            labels={
                  "valor_atual":("Valor atual"),
                  "nome_meta":("Nome da meta financeira"),
            }
            error_messages={
                  "valor_atual":{
                        "invalid":"Preencha apenas com valores numéricos"
                  },
                  "valor_total":{
                        "invalid":"Preencha apenas com valores numéricos"
                  }
            }


class QueryDespesaPorNomeForm(forms.Form):
      nome = forms.CharField()

class QueryDespesaPorDataForm(forms.Form):
      data_inicio = forms.DateField(widget=forms.DateInput(
            attrs={'type':'date','max':datetime.now().date}
      ))
      data_final = forms.DateField(widget=forms.DateInput(
            attrs={'type':'date','max':datetime.now().date}
      ))

class QueryDespesaPorCategoriaForm(forms.Form):
      categoria = forms.ChoiceField(widget=forms.Select,choices=set_choices_categoria())

class LoginForm(forms.Form):
      login = forms.CharField(max_length=100,label="Login")
      password = forms.CharField(widget=forms.PasswordInput,label="Senha")

class CadastroForm(forms.Form):
      login = forms.CharField(max_length=100,label="Login")
      password = forms.CharField(widget=forms.PasswordInput,label="Senha")
      repeat_password = forms.CharField(widget=forms.PasswordInput,label="Repita a senha")
      email = forms.EmailField(label="E-mail")
      