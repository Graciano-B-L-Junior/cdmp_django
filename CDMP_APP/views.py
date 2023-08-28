from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from . import models
from .forms import DespesaForm,DepositoForm,MetaFinanceiraForm
from datetime import datetime

# Create your views here.
def index(request):
    cliente = models.Cliente.objects.all()[0]
    historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
    context = {
        "cliente":cliente,
        "historico_cliente":historico_cliente
    }
    return render(request,'CDMP_APP/index.html',context)

def add_gasto(request):
    if request.method == "POST":
        form = DespesaForm(request.POST)
        if form.is_valid():
            descricao = form.cleaned_data["descricao"]
            valor = form.cleaned_data["valor"]
            data_gasto = form.cleaned_data["data_gasto"]
            categoria = form.cleaned_data["categoria"]
            cliente = models.Cliente.objects.get(nome="Graciano Junior")
            categoria = models.Categoria.objects.get(nome=categoria)
            despesa = models.Despesa(valor=valor,descricao=descricao,data_despesa=data_gasto,cliente=cliente,categoria=categoria)
            historico_cliente = models.HistoricoCliente(cliente=cliente,data_operacao=data_gasto,operacao=descricao,despesa=despesa)
            despesa.save()
            historico_cliente.save()
            return HttpResponseRedirect('/')
        else:
            return render(request,"CDMP_APP/add_gasto.html",{"form":form,"message":"Preencha os campos corretamente"})
    else:
        form = DespesaForm()
    return render(request,"CDMP_APP/add_gasto.html",{"form":form})

def add_deposito(request):
    if request.method == "POST":
        form = DepositoForm(request.POST)
        if form.is_valid():
            deposito:models.Depositos = form.save(commit=False)
            cliente = models.Cliente.objects.get(nome="Graciano Junior")
            deposito.cliente = cliente
            historico_cliente = models.HistoricoCliente(cliente=cliente,data_operacao=deposito.data_deposito,
                                                        deposito=deposito,operacao=deposito.descricao)
            deposito.save()
            historico_cliente.save()

            return HttpResponseRedirect('/')
        else:
            return render(request,"CDMP_APP/add_deposito.html",{"form":form,"message":"Preencha os campos corretamente"})
    else:
        form = DepositoForm()
    return render(request,"CDMP_APP/add_deposito.html",{"form":form})

def add_meta_financeira(request):
    if request.method == "POST":
        form = MetaFinanceiraForm(request.POST)
        if form.is_valid():
            meta_financeira:models.MetaFinanceira = form.save(commit=False)
            cliente = models.Cliente.objects.get(nome="Graciano Junior")
            meta_financeira.cliente = cliente
            historico_cliente = models.HistoricoCliente(cliente=cliente,data_operacao=datetime.now(),
                                                        meta_financeira=meta_financeira,
                                                        operacao=meta_financeira.nome_meta)
            meta_financeira.save()
            historico_cliente.save()

            return HttpResponseRedirect('/')
        else:
            return render(request,"CDMP_APP/add_meta.html",{"form":form,"message":"Preencha os campos corretamente"})
    else:
        form = MetaFinanceiraForm()
        return render(request,"CDMP_APP/add_meta.html",{"form":form,})

def view_meta_financeira(request,id):
    if request.method == "GET":
        
        return render(request,"")
    else:
        return HttpResponseRedirect('/')