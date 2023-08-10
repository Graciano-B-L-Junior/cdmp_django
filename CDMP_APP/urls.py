from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('adicionar_despesa',views.add_gasto,name="add_despesa"),
    path('adicionar_deposito',views.add_deposito,name='add_deposito')
]
