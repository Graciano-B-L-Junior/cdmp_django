from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from . import models
from .forms import GastoForm

# Create your views here.
def index(request):
    cliente = models.Cliente.objects.all()[0]
    context = {
        "cliente":cliente
    }
    return render(request,'CDMP_APP/index.html',context)

def add_gasto(request):
    if request.method == "POST":
        form = GastoForm(request.POST)
        if form.is_valid():
            descricao = form.cleaned_data["descricao"]
            valor = form.cleaned_data["valor"]
            data_gasto = form.cleaned_data["data_gasto"]
            categoria = form.cleaned_data["categoria"]
            cliente = models.Cliente.objects.get(nome="Graciano Junior")
            categoria = models.Categoria.objects.get(nome=categoria)
            Gasto = models.Gasto(valor=valor,descricao=descricao,data_gasto=data_gasto,cliente=cliente,categoria=categoria)
            Gasto.save()
            return HttpResponseRedirect('/')
        else:
            return render(request,"CDMP_APP/add_gasto.html",{"form":form,"message":"Preencha os campos corretamente"})
    else:
        form = GastoForm()
    return render(request,"CDMP_APP/add_gasto.html",{"form":form})