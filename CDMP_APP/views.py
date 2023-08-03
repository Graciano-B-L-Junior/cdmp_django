from django.shortcuts import render
from django.http import HttpResponse
from . import models

# Create your views here.
def index(request):
    cliente = models.Cliente.objects.all()[0]
    context = {
        "cliente":cliente
    }
    return render(request,'CDMP_APP/index.html',context)