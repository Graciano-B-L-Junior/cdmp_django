from django import forms
from datetime import datetime
from .models import Categoria,Receitas,TetoDeGastos

def set_choices_categoria() -> tuple:
        categorias = Categoria.objects.raw("""
            SELECT 
            *
            FROM
            CDMP_APP_categoria
            WHERE (cliente_id IS NULL OR cliente_id = 7);            
            """)
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
    categoria = forms.ChoiceField(widget=forms.Select,choices=set_choices_categoria)

class ReceitasForm(forms.ModelForm):
      class Meta:
            model = Receitas
            fields = ["valor","descricao","data_receita"]
            widgets ={
                  "data_receita":forms.DateInput(attrs={'type':'date','max':datetime.now().date})
            }

class TetoDeGastosForm(forms.ModelForm):
      class Meta:
            model = TetoDeGastos
            fields = ["janeiro","fevereiro","marco",
                      "abril","maio","junho",
                      "julho","agosto","setembro",
                      "outubro","novembro","dezembro"
                      ]
            widgets = {
                  "janeiro":forms.NumberInput(),
                  "fevereiro":forms.NumberInput(),
                  "marco":forms.NumberInput(),
                  "abril":forms.NumberInput(),
                  "maio":forms.NumberInput(),
                  "junho":forms.NumberInput(),
                  "julho":forms.NumberInput(),
                  "agosto":forms.NumberInput(),
                  "setembro":forms.NumberInput(),
                  "outubro":forms.NumberInput(),
                  "novembro":forms.NumberInput(),
                  "dezembro":forms.NumberInput(),
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
      categoria = forms.ChoiceField(widget=forms.Select,choices=set_choices_categoria)

class LoginForm(forms.Form):
      email = forms.EmailField(label="E-mail")
      password = forms.CharField(widget=forms.PasswordInput,label="Senha")

class CadastroForm(forms.Form):
      nome = forms.CharField(max_length=100,label="Nome")
      password = forms.CharField(widget=forms.PasswordInput,label="Senha")
      repeat_password = forms.CharField(widget=forms.PasswordInput,label="Repita a senha")
      email = forms.EmailField(label="E-mail")
      
class CadastroCategoria(forms.ModelForm):
      class Meta:
            model = Categoria
            fields = ["nome"]