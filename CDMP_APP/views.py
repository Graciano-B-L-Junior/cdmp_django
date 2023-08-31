from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from . import models
from .forms import DespesaForm,DepositoForm,MetaFinanceiraForm,QueryDespesaPorNomeForm,QueryDespesaPorDataForm
from datetime import datetime
from typing import List

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

def treat_route(request,id):
    historico = models.HistoricoCliente.objects.get(pk=id)
    if historico.meta_financeira != None:
        return view_meta_financeira(request,id)
    elif historico.despesa != None:
        return view_gasto(request,id)
    elif historico.deposito != None:
        return view_deposito(request,id)
    

def view_meta_financeira(request,id):
    if request.method == "GET":
        meta_financeira = models.HistoricoCliente.objects.get(pk=id).meta_financeira
        cliente = models.Cliente.objects.all()[0]
        historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
        context={
            "nome":meta_financeira.nome_meta,
            "valor_atual":meta_financeira.valor_atual,
            "valor_total":meta_financeira.valor_total,
            "historico_cliente":historico_cliente
        }
        return render(request,"CDMP_APP/view_meta_financeira.html",context)
    else:
        return HttpResponseRedirect('/')
    

def view_despesa(request,id):
    if request.method == "GET":
        despesa = models.HistoricoCliente.objects.get(pk=id).despesa
        cliente = models.Cliente.objects.all()[0]
        historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
        context={
            "nome":despesa.descricao,
            "valor":despesa.valor,
            "data_despesa":despesa.data_despesa.strftime("%d/%m/%Y"),
            "categoria":despesa.categoria.nome,
            "historico_cliente":historico_cliente
        }
        return render(request,"CDMP_APP/view_despesa.html",context)
    else:
        return HttpResponseRedirect('/')


def view_deposito(request,id):
    if request.method == "GET":
        deposito = models.HistoricoCliente.objects.get(pk=id).deposito
        cliente = models.Cliente.objects.all()[0]
        historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
        context={
            "nome":deposito.descricao,
            "valor":deposito.valor,
            "data_despesa":deposito.data_deposito.strftime("%d/%m/%Y"),
            "historico_cliente":historico_cliente
        }
        return render(request,"CDMP_APP/view_deposito.html",context)
    else:
        return HttpResponseRedirect('/')
    

def view_all_despesas(request):
    if request.method == "POST":
        form = QueryDespesaPorNomeForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            cliente = models.Cliente.objects.all()[0]
            historico = models.HistoricoCliente.objects.filter(cliente=cliente.pk,operacao__icontains=nome,despesa__isnull=False).order_by('-id')
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            lista_despesa = []
            for dado in historico:
                lista_despesa.append(dado.despesa)          
        return render(request,"CDMP_APP/view_all_despesas.html",{"form":form,"historico_cliente":historico_cliente,"despesas":lista_despesa})
    else:
        form = QueryDespesaPorNomeForm()
        cliente = models.Cliente.objects.all()[0]
        historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
        return render(request,"CDMP_APP/view_all_despesas.html",{"form":form,"historico_cliente":historico_cliente})


def edit_despesa(request,id):
    if request.method == "GET":
        despesa = models.Despesa.objects.get(pk=id)
        form = DespesaForm(initial={
            "valor":despesa.valor,
            "data_gasto":despesa.data_despesa,
            "descricao":despesa.descricao,
            "categoria":despesa.categoria
        })
                
        cliente = models.Cliente.objects.all()[0]
        historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
        context={
            "form":form,
            "historico_cliente":historico_cliente
        }
        return render(request,"CDMP_APP/add_gasto.html",context)
    else:
        return HttpResponseRedirect('/')