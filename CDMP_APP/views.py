from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from . import models
from .forms import DespesaForm,DepositoForm,MetaFinanceiraForm,\
    QueryDespesaPorNomeForm,QueryDespesaPorDataForm,QueryDespesaPorCategoriaForm,\
    LoginForm,CadastroForm,TetoDeGastosForm
from datetime import datetime
from typing import List
import json



# Create your views here.

def login(request):
    if request.method == "GET":
        form = LoginForm()

        return render(request,"CDMP_APP/login.html",{"form":form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["password"]
            try:
                cliente = models.Cliente.objects.get(email=email,senha=senha)
                request.session["cliente"]=cliente.pk
                return HttpResponseRedirect("/home")
            except:
                messages.error(request,"Email ou senha errados")

        return render(request,"CDMP_APP/login.html",{"form":form})

def cadastro(request):
    if request.method == "GET":
        form = CadastroForm()
        return render(request,"CDMP_APP/cadastrar_conta.html",{"form":form})
    elif request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            password = form.cleaned_data["password"]
            repeat_password = form.cleaned_data["repeat_password"]
            email = form.cleaned_data["email"]
            if password != repeat_password:
                messages.error(request,"As senhas precisam ser iguais")
            else:
                cliente = models.Cliente()
                cliente.nome = nome
                cliente.email = email
                cliente.senha = password
                cliente.save()
                messages.info(request,"Conta criada com sucesso!")
                return HttpResponseRedirect('/')

        return render(request,"CDMP_APP/cadastrar_conta.html",{"form":form})

def logoff(request):
    request.session.pop("cliente")
    return HttpResponseRedirect("/")

def index(request):
    cliente = request.session.get("cliente")
    if cliente != None:
        cliente = models.Cliente.objects.get(pk=cliente)
        historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
        context = {
            "cliente":cliente,
            "historico_cliente":historico_cliente
        }
        return render(request,'CDMP_APP/index.html',context)
    else:
        return HttpResponseRedirect("/")

def add_gasto(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "POST":
            form = DespesaForm(request.POST)
            if form.is_valid():
                descricao = form.cleaned_data["descricao"]
                valor = form.cleaned_data["valor"]
                data_gasto = form.cleaned_data["data_despesa"]
                categoria = form.cleaned_data["categoria"]
                cliente = models.Cliente.objects.get(pk=cliente)
                categoria = models.Categoria.objects.get(nome=categoria)
                despesa = models.Despesa(valor=valor,descricao=descricao,data_despesa=data_gasto,cliente=cliente,categoria=categoria)
                historico_cliente = models.HistoricoCliente(cliente=cliente,data_operacao=data_gasto,operacao=descricao,despesa=despesa)
                despesa.save()
                historico_cliente.save()
                return HttpResponseRedirect('/home')
            else:
                cliente = models.Cliente.objects.get(pk=cliente)
                historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
                return render(request,"CDMP_APP/add_gasto.html",{"form":form,
                                                                "historico_cliente":historico_cliente,
                                                                "message":"Preencha os campos corretamente"})
        else:
            form = DespesaForm()
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
        return render(request,"CDMP_APP/add_gasto.html",{"form":form,"historico_cliente":historico_cliente})
    else:
        return HttpResponseRedirect("/")

def add_deposito(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "POST":
            form = DepositoForm(request.POST)
            if form.is_valid():
                deposito:models.Depositos = form.save(commit=False)
                cliente = models.Cliente.objects.get(pk=cliente)
                deposito.cliente = cliente
                historico_cliente = models.HistoricoCliente(cliente=cliente,data_operacao=deposito.data_deposito,
                                                            deposito=deposito,operacao=deposito.descricao)
                deposito.save()
                historico_cliente.save()

                return HttpResponseRedirect('/home')
            else:
                cliente = models.Cliente.objects.get(pk=cliente)
                historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
                return render(request,"CDMP_APP/add_deposito.html",{"form":form,
                                                                    "historico_cliente":historico_cliente,
                                                                    "message":"Preencha os campos corretamente"})
        else:
            form = DepositoForm()
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
        return render(request,"CDMP_APP/add_deposito.html",{"form":form,
                                                            "historico_cliente":historico_cliente})
    else:
        return HttpResponseRedirect("/")

def add_meta_financeira(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "POST":
            form = MetaFinanceiraForm(request.POST)
            if form.is_valid():
                meta_financeira:models.MetaFinanceira = form.save(commit=False)
                cliente = models.Cliente.objects.get(pk=cliente)
                meta_financeira.cliente = cliente
                historico_cliente = models.HistoricoCliente(cliente=cliente,data_operacao=datetime.now(),
                                                            meta_financeira=meta_financeira,
                                                            operacao=meta_financeira.nome_meta)
                meta_financeira.save()
                historico_cliente.save()

                return HttpResponseRedirect('/home')
            else:
                cliente = models.Cliente.objects.get(pk=cliente)
                historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
                return render(request,"CDMP_APP/add_meta.html",{"form":form,
                                                                "historico_cliente":historico_cliente,
                                                                "message":"Preencha os campos corretamente"})
        else:
            form = MetaFinanceiraForm()
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            return render(request,"CDMP_APP/add_meta.html",{"form":form,
                                                            "historico_cliente":historico_cliente})
    else:
        return HttpResponseRedirect("/")
    
def add_teto_gasto(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "GET":
            form = TetoDeGastosForm()
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            return render(request,"CDMP_APP/add_teto_gasto.html",{"form":form,
                                                            "historico_cliente":historico_cliente})
        elif request.method == "POST":
            geral = request.POST.get("geral")
            if geral !=None:
                pass
            else:
                pass
    else:
        return HttpResponseRedirect("/")

def treat_route(request,id):
    cliente = request.session.get("cliente")
    if cliente !=None:
        historico = models.HistoricoCliente.objects.get(pk=id)
        if historico.meta_financeira != None:
            return view_meta_financeira(request,id)
        elif historico.despesa != None:
            return view_despesa(request,id)
        elif historico.deposito != None:
            return view_deposito(request,id)
    else:
        return HttpResponseRedirect("/")
    
def view_meta_financeira(request,id):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "GET":
            meta_financeira = models.HistoricoCliente.objects.get(pk=id).meta_financeira
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            context={
                "nome":meta_financeira.nome_meta,
                "valor_atual":meta_financeira.valor_atual,
                "valor_total":meta_financeira.valor_total,
                "historico_cliente":historico_cliente
            }
            return render(request,"CDMP_APP/view_meta_financeira.html",context)
        else:
            request.session.pop("cliente")
            return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect("/")
    
def view_despesa(request,id):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "GET":
            despesa = models.HistoricoCliente.objects.get(pk=id).despesa
            cliente = models.Cliente.objects.get(pk=cliente)
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
            request.session.pop("cliente")
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect("/")

def view_deposito(request,id):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "GET":
            deposito = models.HistoricoCliente.objects.get(pk=id).deposito
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            context={
                "nome":deposito.descricao,
                "valor":deposito.valor,
                "data_despesa":deposito.data_deposito.strftime("%d/%m/%Y"),
                "historico_cliente":historico_cliente
            }
            return render(request,"CDMP_APP/view_deposito.html",context)
        else:
            request.session.pop("cliente")
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect("/")
    

def view_despesa(request,id):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "GET":
            despesa = models.HistoricoCliente.objects.get(pk=id).despesa
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            context={
                "nome":despesa.descricao,
                "valor":despesa.valor,
                "data_despesa":despesa.data_despesa.strftime("%d/%m/%Y"),
                "categoria":despesa.categoria,
                "historico_cliente":historico_cliente
            }
            return render(request,"CDMP_APP/view_despesa.html",context)
        else:
            request.session.pop("cliente")
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect("/")
    
def view_all_despesas(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        page_redirect=""
        if request.method == "POST":
            form = QueryDespesaPorNomeForm(request.POST)
            if form.is_valid():
                page_redirect="?page=vizualizar_gastos"
                nome = form.cleaned_data["nome"]
                cliente = models.Cliente.objects.get(pk=cliente)
                historico = models.HistoricoCliente.objects.filter(cliente=cliente.pk,operacao__icontains=nome,despesa__isnull=False).order_by('-id')
                historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
                lista_despesa = []
                for dado in historico:
                    lista_despesa.append(dado.despesa)          
            return render(request,"CDMP_APP/view_all_despesas.html",{"form":form,"historico_cliente":historico_cliente,"despesas":lista_despesa,"page":page_redirect})
        else:
            form = QueryDespesaPorNomeForm()
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            return render(request,"CDMP_APP/view_all_despesas.html",{"form":form,"historico_cliente":historico_cliente})
    else:
        return HttpResponseRedirect("/")

def edit_despesa(request,id):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "GET":
            despesa = models.Despesa.objects.get(pk=id)
            form = DespesaForm(initial={
                "valor":despesa.valor,
                "data_despesa":despesa.data_despesa,
                "descricao":despesa.descricao,
                "categoria":despesa.categoria
            })
                    
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            context={
                "form":form,
                "historico_cliente":historico_cliente
            }
            return render(request,"CDMP_APP/edit_despesa.html",context)
        elif request.method == "POST":
            form = DespesaForm(request.POST)
            despesa = models.Despesa.objects.get(pk=id)
            if form.is_valid():
                despesa.valor = form.cleaned_data["valor"]
                despesa.categoria =  models.Categoria.objects.get(nome=form.cleaned_data["categoria"])
                despesa.descricao = form.cleaned_data["descricao"]
                despesa.data_despesa = form.cleaned_data["data_despesa"]
                despesa.save()
                page = request.GET.get("page")

                return HttpResponseRedirect(f"/{page}")

            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            context={
                "form":form,
                "historico_cliente":historico_cliente
            }
            return render(request,"CDMP_APP/edit_despesa.html",context)
    else:
        return HttpResponseRedirect("/")
    
def view_despesa_por_categoria(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        page_redirect=""
        if request.method == "GET":
            form = QueryDespesaPorCategoriaForm()
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente).order_by('-id')[:5]
            return render(request,"CDMP_APP/view_despesa_por_categoria.html",{"form":form,"historico_cliente":historico_cliente})
        elif request.method == "POST":
            page_redirect="?page=visualizar_despesas_por_categoria"
            form = QueryDespesaPorCategoriaForm(request.POST)
            if form.is_valid():
                categoria = form.cleaned_data["categoria"]
                cliente = models.Cliente.objects.get(pk=cliente)
                historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente).order_by('-id')[:5]
                categoria = models.Categoria.objects.get(nome=categoria)
                despesa = models.HistoricoCliente.objects.filter(cliente=cliente,despesa__isnull=False).only('despesa')
                despesa = models.Despesa.objects.filter(id__in=despesa.values('despesa'),categoria=categoria)
                return render(request,"CDMP_APP/view_despesa_por_categoria.html",{"form":form,
                                                                                "historico_cliente":historico_cliente,
                                                                                "despesas":despesa,
                                                                                "page":page_redirect})
            else:
                cliente = models.Cliente.objects.get(pk=cliente)
                historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
                return render(request,"CDMP_APP/view_despesa_por_categoria.html",{"form":form,"historico_cliente":historico_cliente})
    else:
        return HttpResponseRedirect("/")
    
def view_despesa_por_data(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        page_redirect=""
        if request.method == "GET":
            form = QueryDespesaPorDataForm()
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            return render(request,"CDMP_APP/view_despesa_por_data.html",{"form":form,"historico_cliente":historico_cliente})
        elif request.method == "POST":
            page_redirect="?page=visualizar_despesa_por_data"
            form = QueryDespesaPorDataForm(request.POST)
            if form.is_valid():
                data_inicio = form.cleaned_data["data_inicio"]
                data_fim = form.cleaned_data["data_final"]
                if data_inicio > data_fim:
                    messages.error(request,"data inicio não pode ser maior que a data final")
                    #messages.error(request,"data inicio não pode maior que a data final")
                cliente = models.Cliente.objects.get(pk=cliente)
                historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
                despesa = models.HistoricoCliente.objects.filter(cliente=cliente.pk,despesa__isnull=False,
                                                                 data_operacao__lte=data_fim,
                                                                 data_operacao__gte=data_inicio)\
                                                                    .only('despesa').order_by('-data_operacao')
                despesas = []
                for d in despesa:
                    despesas.append(d.despesa)
                
                return render(request,"CDMP_APP/view_despesa_por_data.html",{"form":form,
                                                                            "historico_cliente":historico_cliente,
                                                                            "despesas":despesas,
                                                                            "page":page_redirect})
            else:
                cliente = models.Cliente.objects.get(pk=cliente)
                historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
                return render(request,"CDMP_APP/view_despesa_por_data.html",{"form":form,"historico_cliente":historico_cliente})
        else:
            return HttpResponseRedirect("/")

def get_despesas_agrupadas_por_mes_grafico(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "GET":
            cliente = models.Cliente.objects.get(pk=cliente)
            print(cliente)
            start_date:datetime = datetime(datetime.now().year,1,1)
            end_date:datetime = datetime.now()
            historico = models.HistoricoCliente.objects.filter(cliente=cliente,
                                                               despesa__isnull=False,
                                                               deposito__isnull=True,
                                                               meta_financeira__isnull=True,
                                                             data_operacao__range=(start_date,end_date)).order_by("data_operacao")
            lista={}
            lista["labels"]=['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul','ago', 'set', 'out', 'nov', 'dez']

            for index,mes in enumerate(lista["labels"]):
                lista[f"{index+1}-{mes}"]=0
            valor_despesa=0
            mes_atual=0
            for index,dado in enumerate(historico):
                if index==0:
                    mes_atual = dado.despesa.data_despesa.month
                    valor_despesa+=dado.despesa.valor
                    lista[
                        f"{mes_atual}-{lista['labels'][mes_atual-1]}"
                        ]=valor_despesa
                else:
                    if mes_atual == dado.despesa.data_despesa.month:
                        valor_despesa+=dado.despesa.valor
                        lista[
                            f"{mes_atual}-{lista['labels'][mes_atual-1]}"
                              ]=valor_despesa
                    else:
                        mes_atual = dado.despesa.data_despesa.month
                        valor_despesa= dado.despesa.valor
                        lista[
                            f"{mes_atual}-{lista['labels'][mes_atual-1]}"
                              ]=valor_despesa
                        print(valor_despesa)
            return HttpResponse(json.dumps(lista,indent=4))
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)