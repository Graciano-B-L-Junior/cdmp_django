from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    senha = models.CharField(default="",max_length=100)
    email = models.EmailField()
    foto = models.CharField(default="default.jpg",blank=True,null=True,max_length=100)
    def __str__(self) -> str:
        return self.nome
    class Meta:
        verbose_name="Cliente"
        verbose_name_plural="Clientes"

class Categoria(models.Model):
    nome = models.CharField(unique=True,max_length=50)
    data_criacao = models.DateTimeField(default=timezone.now)
    cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE)

    class Meta:
        verbose_name="Categoria"
        verbose_name_plural="Categorias"

    def __str__(self) -> str:
        return self.nome
class Despesa(models.Model):
    valor = models.FloatField()
    descricao = models.CharField(max_length=50)
    data_despesa = models.DateTimeField(default=timezone.now)
    cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria,null=True,on_delete=models.SET_NULL)
    class Meta:
        verbose_name="Despesa"
        verbose_name_plural="Despesas"

    def __str__(self) -> str:
        return self.descricao
    
class Receitas(models.Model):
    valor = models.FloatField()
    descricao = models.CharField(max_length=50)
    data_receita = models.DateTimeField(default=timezone.now)
    cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE)
    class Meta:
        verbose_name="Receita"
        verbose_name_plural="Receitas"

    def __str__(self) -> str:
        return self.descricao

class HistoricoCliente(models.Model):
    cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE)
    despesa = models.ForeignKey(Despesa,null=True,on_delete=models.CASCADE)
    receita = models.ForeignKey(Receitas,null=True,on_delete=models.CASCADE)
    operacao = models.CharField(max_length=100)
    data_operacao = models.DateTimeField()
    class Meta:
        verbose_name="HistoricoCliente"
        verbose_name_plural="HistoricoClientes"

    def __str__(self) -> str:
        return self.operacao

class TetoDeGastos(models.Model):
        cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE)
        janeiro = models.FloatField(default=0)
        fevereiro = models.FloatField(default=0)
        marco = models.FloatField(default=0)
        abril = models.FloatField(default=0)
        maio = models.FloatField(default=0)
        junho = models.FloatField(default=0)
        julho = models.FloatField(default=0)
        agosto = models.FloatField(default=0)
        setembro = models.FloatField(default=0)
        outubro = models.FloatField(default=0)
        novembro = models.FloatField(default=0)
        dezembro = models.FloatField(default=0)

        def __str__(self) -> str:
            return f"Teto de gastos cliente: {self.cliente}"
        

class TetoDeGastosPorCategoria(models.Model):
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    teto = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"Teto de gastos da categoria: {self.categoria}"