from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('adicionar_despesa',views.add_gasto,name="add_despesa"),
    path('adicionar_deposito',views.add_deposito,name='add_deposito'),
    path('adicionar_meta',views.add_meta_financeira,name="add_meta"),
    path('vizualizar_historico/<int:id>',views.treat_route,name="view_history")
]
