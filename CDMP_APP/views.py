from django import forms
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages

from CDMP_APP.scripts.get_despesas_by_user import get_all_despesas_by_user
from . import models
from .forms import DespesaForm, FormSelectFielCategoryByClient,ReceitasForm,\
    QueryDespesaPorNomeForm,QueryDespesaPorDataForm,QueryDespesaPorCategoriaForm,\
    LoginForm,CadastroForm,TetoDeGastosForm,CadastroCategoria,TetoDeGastosCategoriaForm
from datetime import datetime,timedelta
from .scripts.generate_categories_for_client import generate_Categories
from .scripts.aux_teto_cliente_update import update_teto_gastos,update_teto_gastos_por_geral
import json
from django.db.models import Sum
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
                models.TetoDeGastos(cliente=cliente).save()
                generate_Categories(cliente)
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
        despesas = get_all_despesas_by_user(request)
        context = {
            "cliente":cliente,
            "historico_cliente":historico_cliente,
            "despesas":despesas
        }
        return render(request,'CDMP_APP/index.html',context)
    else:
        return HttpResponseRedirect("/")

def add_gasto(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "POST":
            form = DespesaForm(cliente,request.POST,)
            if form.is_valid():
                descricao = form.cleaned_data["descricao"]
                valor = form.cleaned_data["valor"]
                data_gasto = form.cleaned_data["data_despesa"]
                categoria = form.cleaned_data["categoria"]
                cliente = models.Cliente.objects.get(pk=cliente)
                categoria = models.Categoria.objects.get(nome=categoria,cliente=cliente)
                aux_valor = float(valor)
                if aux_valor < 0:
                    messages.error(request,"valor negativo não permitido!")
                    historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
                    return render(request,"CDMP_APP/add_gasto.html",{"form":form,
                                                                    "historico_cliente":historico_cliente,
                                                                    "message":"Preencha os campos corretamente"})
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
            form = DespesaForm(cliente_id=cliente)
            
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
        return render(request,"CDMP_APP/add_gasto.html",{"form":form,"historico_cliente":historico_cliente})
    else:
        return HttpResponseRedirect("/")

def add_receita(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "POST":
            form = ReceitasForm(request.POST)
            if form.is_valid():
                receita:models.Receitas = form.save(commit=False)
                cliente = models.Cliente.objects.get(pk=cliente)
                receita.cliente = cliente
                historico_cliente = models.HistoricoCliente(cliente=cliente,data_operacao=receita.data_receita,
                                                            receita=receita,operacao=receita.descricao)
                receita.save()
                historico_cliente.save()

                return HttpResponseRedirect('/home')
            else:
                cliente = models.Cliente.objects.get(pk=cliente)
                historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
                return render(request,"CDMP_APP/add_deposito.html",{"form":form,
                                                                    "historico_cliente":historico_cliente,
                                                                    "message":"Preencha os campos corretamente"})
        else:
            form = ReceitasForm()
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
        return render(request,"CDMP_APP/add_deposito.html",{"form":form,
                                                            "historico_cliente":historico_cliente})
    else:
        return HttpResponseRedirect("/")

    
def add_teto_gasto(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "GET":
            cliente = models.Cliente.objects.get(pk=cliente)
            teto_cliente = models.TetoDeGastos.objects.get(cliente=cliente)
            form = TetoDeGastosForm(instance=teto_cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            return render(request,"CDMP_APP/edit_teto_gasto.html",{"form":form,
                                                            "historico_cliente":historico_cliente})
        elif request.method == "POST":
            geral = request.POST.get("geral")
            if geral !=None:
                cliente = models.Cliente.objects.get(pk=cliente)
                teto_cliente = models.TetoDeGastos.objects.get(cliente=cliente)
                try:
                    valor_geral = float(request.POST.get("geral"))
                    update_teto_gastos_por_geral(teto_cliente,valor_geral)
                    teto_cliente.save()
                    messages.success(request, "Teto de gastos atualizado com sucesso")
                except Exception as error:
                    messages.error(request, "Ocorreu um erro ao atualizar os dados, tente novamente")
                    return HttpResponseRedirect("/editar_teto")
                
                return HttpResponseRedirect("/editar_teto")
                
            else:
                form = TetoDeGastosForm(request.POST)
                if form.is_valid():
                    cliente = models.Cliente.objects.get(pk=cliente)
                    teto_cliente = models.TetoDeGastos.objects.get(cliente=cliente)
                    form_teto:models.TetoDeGastos = form.save(commit=False)
                    update_teto_gastos(teto_cliente,form_teto)
                    teto_cliente.save()
                    messages.success(request, "Teto de gastos atualizado com sucesso")
                    return HttpResponseRedirect("/editar_teto")
                else:
                    cliente = models.Cliente.objects.get(pk=cliente)
                    historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
                    return render(request,"CDMP_APP/edit_teto_gasto.html",{"form":form,
                                                            "historico_cliente":historico_cliente})
    else:
        return HttpResponseRedirect("/")

def set_teto_categoria(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "GET" and request.GET.get("categoria") == None:
            form = FormSelectFielCategoryByClient(cliente)
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            return render(request,"CDMP_APP/set_teto_category.html",{"form":form,
                                                            "historico_cliente":historico_cliente})
        elif request.method == "GET" and request.GET.get("categoria") != None:
            cliente = models.Cliente.objects.get(pk=cliente)
            categoria =models.Categoria.objects.get(
                cliente=cliente,
                nome=request.GET.get("categoria")
            )
            teto = models.TetoDeGastosPorCategoria(cliente=cliente,categoria=categoria)
            form = TetoDeGastosCategoriaForm(instance=teto)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            return render(request,"CDMP_APP/set_teto_category.html",{
                                                            "form":form,
                                                            "form_post":True,
                                                            "categoria_nome_input_hidden":categoria.nome,
                                                            "categoria_texto":f"Categoria selecionada: {categoria.nome}",
                                                            "historico_cliente":historico_cliente})
        elif request.method == "POST":
            form = TetoDeGastosCategoriaForm(request.POST)
            if form.is_valid():
                cliente = models.Cliente.objects.get(pk=cliente)
                categoria =models.Categoria.objects.get(
                    cliente=cliente,
                    nome=request.POST.get("categoria")
                )
                teto_categoria = models.TetoDeGastosPorCategoria.objects.get(cliente=cliente,categoria=categoria)
                teto_categoria.teto = request.POST.get("teto")
                teto_categoria.save()
                messages.success(request,f"Teto da categoria {teto_categoria.categoria.nome} definida com sucesso!")
                return HttpResponseRedirect("/editar_teto_categoria")
    else:
        return HttpResponseRedirect("/")

def treat_route(request,id):
    cliente = request.session.get("cliente")
    if cliente !=None:
        historico = models.HistoricoCliente.objects.get(pk=id)
        if historico.despesa != None:
            return view_despesa(request,id)
        elif historico.receita != None:
            return view_deposito(request,id)
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
            receita = models.HistoricoCliente.objects.get(pk=id).receita
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            context={
                "nome":receita.descricao,
                "valor":receita.valor,
                "data_despesa":receita.data_receita.strftime("%d/%m/%Y"),
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
            form = DespesaForm(cliente,initial={
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
                if despesa.valor < 0:
                    messages.error(request,"valor negativo não permitido!")
                    cliente = models.Cliente.objects.get(pk=cliente)
                    historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
                    context={
                            "form":form,
                            "historico_cliente":historico_cliente
                        }
                    return render(request,"CDMP_APP/edit_despesa.html",context)
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

def cadastrar_categoria(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "GET":
            form = CadastroCategoria()
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
            return render(request,"CDMP_APP/cadastro_categoria.html",{
                "form":form,"historico_cliente":historico_cliente
            })
        elif request.method == "POST":
            form = CadastroCategoria(request.POST)
            if form.is_valid():
                nome = form.cleaned_data["nome"]
                new_categoria = models.Categoria()
                new_categoria.nome = nome
                new_categoria.data_criacao = datetime.now()
                cliente = models.Cliente.objects.get(pk=cliente)
                new_categoria.cliente = cliente
                messages.success(request,"Categoria criada com sucesso")
                new_categoria.save()
                return HttpResponseRedirect("/adicionar_categoria")
            else:
                cliente = models.Cliente.objects.get(pk=cliente)
                historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente.pk).order_by('-id')[:5]
                return render(request,"CDMP_APP/cadastro_categoria.html",{
                "form":form,"historico_cliente":historico_cliente
                })

    else:
        return HttpResponseRedirect("/")

def view_despesa_por_categoria(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        page_redirect=""
        if request.method == "GET":
            form = QueryDespesaPorCategoriaForm(cliente_id=cliente)
            cliente = models.Cliente.objects.get(pk=cliente)
            historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente).order_by('-id')[:5]
            return render(request,"CDMP_APP/view_despesa_por_categoria.html",{"form":form,"historico_cliente":historico_cliente})
        elif request.method == "POST":
            page_redirect="?page=visualizar_despesas_por_categoria"
            form = QueryDespesaPorCategoriaForm(cliente,request.POST)
            if form.is_valid():
                categoria = form.cleaned_data["categoria"]
                cliente = models.Cliente.objects.get(pk=cliente)
                historico_cliente = models.HistoricoCliente.objects.filter(cliente=cliente).order_by('-id')[:5]
                categoria = models.Categoria.objects.get(nome=categoria,cliente=cliente)
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
            teto_gasto = models.TetoDeGastos.objects.get(cliente=cliente)
            start_date:datetime = datetime(datetime.now().year,1,1)
            end_date:datetime = datetime.now()
            historico = models.HistoricoCliente.objects.filter(cliente=cliente,
                                                               despesa__isnull=False,
                                                               receita__isnull=True,                                                            
                                                             data_operacao__range=(start_date,end_date))\
                                                            .order_by("data_operacao")
            lista={}
            lista["labels"]=['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul','ago', 'set', 'out', 'nov', 'dez']
            lista["teto_gasto_cliente"]=[
                teto_gasto.janeiro,teto_gasto.fevereiro,teto_gasto.marco,
                teto_gasto.abril,teto_gasto.maio,teto_gasto.junho,
                teto_gasto.julho,teto_gasto.agosto,teto_gasto.setembro,
                teto_gasto.outubro,teto_gasto.novembro,teto_gasto.dezembro
            ]
            

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
            return HttpResponse(json.dumps(lista,indent=4))
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)
    
def get_economia_despesas_agrupadas_por_mes_grafico(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "GET":
            cliente = models.Cliente.objects.get(pk=cliente)
            teto_gasto = models.TetoDeGastos.objects.get(cliente=cliente)
            start_date:datetime = datetime(datetime.now().year,1,1)
            end_date:datetime = datetime.now().replace(day=1) - timedelta(days=1)            
            historico = models.HistoricoCliente.objects.filter(cliente=cliente,
                                                               despesa__isnull=False,
                                                               receita__isnull=True,                                                               
                                                             data_operacao__range=(start_date,end_date))\
                                                            .order_by("data_operacao")
            lista_aux={}
            lista_result={}
            lista_result["labels"]=['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul','ago', 'set', 'out', 'nov', 'dez']
            lista_aux["labels"]=lista_result["labels"]
            lista_result["economias"]=[]
            lista_aux["teto_gasto_cliente"]=[
                teto_gasto.janeiro,teto_gasto.fevereiro,teto_gasto.marco,
                teto_gasto.abril,teto_gasto.maio,teto_gasto.junho,
                teto_gasto.julho,teto_gasto.agosto,teto_gasto.setembro,
                teto_gasto.outubro,teto_gasto.novembro,teto_gasto.dezembro
            ]
            

            for index,mes in enumerate(lista_aux["labels"]):
                lista_aux[f"{index+1}-{mes}"]=0
            valor_despesa=0
            mes_atual=0
            for index,dado in enumerate(historico):
                
                if index==0:
                    mes_atual = dado.despesa.data_despesa.month
                    valor_despesa+=dado.despesa.valor
                    lista_aux[
                        f"{mes_atual}-{lista_aux['labels'][mes_atual-1]}"
                        ]=valor_despesa
                else:
                    if mes_atual == dado.despesa.data_despesa.month:
                        valor_despesa+=dado.despesa.valor
                        lista_aux[
                            f"{mes_atual}-{lista_aux['labels'][mes_atual-1]}"
                              ]=valor_despesa
                    else:
                        mes_atual = dado.despesa.data_despesa.month
                        valor_despesa= dado.despesa.valor
                        lista_aux[
                            f"{mes_atual}-{lista_aux['labels'][mes_atual-1]}"
                              ]=valor_despesa
            
            for index,mes in enumerate(lista_aux["labels"]):
                if lista_aux[f"{index+1}-{mes}"]==0:
                    lista_result["economias"].append(0)
                else:
                    lista_result["economias"].append(
                        lista_aux["teto_gasto_cliente"][index]-lista_aux[f"{index+1}-{mes}"]
                    )
            return HttpResponse(json.dumps(lista_result,indent=4))
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)
    
def get_gastos_por_categoria(request):
    cliente = request.session.get("cliente")
    if cliente !=None:
        if request.method == "GET":
            cliente=models.Cliente.objects.get(pk=cliente)
            categorias_cliente=models.Categoria.objects.filter(
                cliente_id=cliente
            )
            end_date=datetime.now()
            start_date=datetime(end_date.year,end_date.month,1)
            despesas=models.Despesa.objects.filter(
                cliente_id=cliente,
                categoria_id__in=categorias_cliente,
                data_despesa__lte=end_date,
                data_despesa__gte=start_date
            ).values('categoria__nome').annotate(soma=Sum('valor'))
            
            res_json={}
            for x in despesas:
                res_json[x["categoria__nome"]]=x["soma"]

            return HttpResponse(json.dumps(res_json),content_type='application/json')
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)
    
def get_gastos_categoria_x_teto_gastos_categoria(request):
    cliente = request.session.get("cliente")
    if cliente!=None:
        if request.method == "GET":
            cliente=models.Cliente.objects.get(pk=cliente)
            categorias_cliente=models.Categoria.objects.filter(
                cliente_id=cliente
            )
            
            teto_por_categoria = models.TetoDeGastosPorCategoria.objects.filter(
                cliente=cliente,
                categoria__in=categorias_cliente
            )
            
            start_date=datetime.now().replace(day=1)
            end_date=datetime.now()
            print(end_date,start_date)
            despesas=models.Despesa.objects.filter(
                cliente_id=cliente,
                categoria_id__in=categorias_cliente,
                data_despesa__lte=end_date,
                data_despesa__gte=start_date
            ).values('categoria','valor',).annotate(total=Sum('valor'))
            print("ronaldinho soccer")
            print(despesas)
            res_json={}
            for teto in teto_por_categoria:
                for despesa in despesas:
                    if teto.categoria.pk == despesa["categoria"]:
                        res_json[teto.categoria.nome]={
                            "teto":teto.teto,
                            "gastos":despesa["valor"]
                        }
            
            return HttpResponse(json.dumps(res_json),content_type='application/json')
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)

#verificar o que fazer depois com essa requisição
# def get_all_despesas(request):
#     cliente = request.session.get("cliente")
#     if cliente!=None:
#         historicos = models.HistoricoCliente.objects.filter(
#             cliente=models.Cliente.objects.get(pk=cliente),
#             despesa__isnull=False,
#             receita__isnull=True,
#         )
#         response={}
#         for historico in historicos:
#             response[historico.despesa.pk]={
#                 "descricao":historico.despesa.descricao,
#                 "valor":historico.despesa.valor,
#                 "data":historico.despesa.data_despesa.strftime("%d-%m-%Y"),
#                 "categoria":historico.despesa.categoria.nome,
#                 "historico_id":historico.pk
#             }
#         return HttpResponse(json.dumps(response,ensure_ascii=False),content_type='application/json')
#     else:
#         return HttpResponse(status=404)
