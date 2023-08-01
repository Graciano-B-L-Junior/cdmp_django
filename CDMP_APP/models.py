from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(unique=True,max_length=50)
    data_criacao = models.DateTimeField(default=timezone.now)

class Gasto(models.Model):
    valor = models.FloatField()
    descricao = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria,null=True,blank=True,on_delete=models.SET_NULL)
    data_gasto = models.DateTimeField(default=timezone.now)

class Depositos(models.Model):
    valor = models.FloatField()
    descricao = models.CharField(max_length=50)
    data_deposito = models.DateTimeField(default=timezone.now)

class MetaFinanceira(models.Model):
    nome_meta = models.CharField(max_length=50)
    valor_atual = models.FloatField()
    icone = models.CharField(max_length=50)
    valor_total = models.FloatField()

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    gastos = models.ForeignKey(Gasto,blank=True,null=True,on_delete=models.SET_NULL)
    depositos = models.ForeignKey(Depositos,blank=True,null=True,on_delete=models.SET_NULL)
    metas = models.ForeignKey(MetaFinanceira,blank=True,null=True,on_delete=models.SET_NULL)
    foto = models.CharField(default="default.jpg",blank=True,null=True,max_length=100)

class HistoricoModificaoes(models.Model):
    gasto_fk = models.ForeignKey(Gasto,on_delete=models.CASCADE)
    data_alteracao =models.DateTimeField(default=timezone.now)
    nome = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria,on_delete=models.SET_NULL,null=True)
    valor = models.FloatField()
    