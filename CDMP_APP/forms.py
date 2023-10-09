from collections.abc import Mapping
from typing import Any
from django import forms
from datetime import datetime
from django.core.files.base import File
from django.db.models.base import Model

from django.forms.utils import ErrorList
from .models import Categoria,Receitas,TetoDeGastos,TetoDeGastosPorCategoria



class DespesaForm(forms.Form):
    def set_choices_categoria(self,cliente) -> tuple:
        categorias = Categoria.objects.filter(
              cliente__pk=cliente
        )
        tupla= tuple()
        lista=[]
        for categoria in categorias:
              lista.append(categoria.nome)
        tupla = ((categoria,categoria) for categoria in lista)
        return tupla
    def __init__(self,cliente_id="",*args,**kwargs) -> None:
      super().__init__(*args,**kwargs)
      if cliente_id !="":
            self.fields["categoria"] = forms.ChoiceField(widget=forms.Select,choices=self.set_choices_categoria(cliente_id))
      else:
            raise Exception("cliente_id cannot be empty")
      
    valor = forms.FloatField(error_messages={"invalid":"Preencha o campo apenas com números"})
    descricao = forms.CharField(max_length=50)
    data_despesa = forms.DateField(widget=forms.DateInput(attrs={'type':'date','max':datetime.now().date}))
    categoria = forms.ChoiceField(widget=forms.Select)

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

class TetoDeGastosCategoriaForm(forms.ModelForm):
      def __init__(self, *args,**kwargs) -> None:
            super().__init__(*args,**kwargs)

      class Meta:
            model = TetoDeGastosPorCategoria
            fields = ["teto"]
            widgets = {
                  "teto":forms.NumberInput(),
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
      def set_choices_categoria(self,cliente) -> tuple:
        categorias = Categoria.objects.filter(
              cliente__pk=cliente
        )
        tupla= tuple()
        lista=[]
        for categoria in categorias:
              lista.append(categoria.nome)
        tupla = ((categoria,categoria) for categoria in lista)
        return tupla
      def __init__(self,cliente_id="",*args,**kwargs) -> None:
            super().__init__(*args,**kwargs)
            if cliente_id !="":
                  self.fields["categoria"] = forms.ChoiceField(widget=forms.Select,choices=self.set_choices_categoria(cliente_id))
            else:
                  raise Exception("cliente_id cannot be empty")
      categoria = forms.ChoiceField(widget=forms.Select,choices="")

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

class FormSelectFielCategoryByClient(forms.Form):
      def __init__(self,cliente_id="",*args,**kwargs) -> None:
            super().__init__(*args,**kwargs)
            if cliente_id !="":
                  self.fields["categoria"] = forms.ChoiceField(widget=forms.Select,choices=self.set_choices_categoria(cliente_id))
            else:
                  raise Exception("cliente_id cannot be empty")
            
      def set_choices_categoria(self,cliente) -> tuple:
        categorias = Categoria.objects.filter(
              cliente__pk=cliente
        )
        tupla= tuple()
        lista=[]
        for categoria in categorias:
              lista.append(categoria.nome)
        tupla = ((categoria,categoria) for categoria in lista)
        return tupla
      categoria = forms.ChoiceField(widget=forms.Select,choices="")