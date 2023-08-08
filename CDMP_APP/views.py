from django.shortcuts import render
from django.http import HttpResponse
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
        pass
    else:
        form = GastoForm()
    return render(request,"CDMP_APP/add_gasto.html",{"form":form})