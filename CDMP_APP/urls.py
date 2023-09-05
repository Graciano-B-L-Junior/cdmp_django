from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('adicionar_despesa',views.add_gasto,name="add_despesa"),
    path('adicionar_deposito',views.add_deposito,name='add_deposito'),
    path('adicionar_meta',views.add_meta_financeira,name="add_meta"),
    path('vizualizar_historico/<int:id>',views.treat_route,name="view_history"),
    path('vizualizar_gastos',views.view_all_despesas,name="view_all_gastos"),
    path('editar_despesa/<int:id>',views.edit_despesa,name="edit_despesa"),
    path('visualizar_despesas_por_categoria',views.view_despesa_por_categoria,name="despesa_por_categoria"),
    path('visualizar_despesa_por_data',views.view_despesa_por_data,name="despesa_por_data")
]
