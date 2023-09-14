from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('cadastrar_conta',views.cadastro,name='cadastrar'),
    path('home',views.index,name='index'),
    path('sair',views.logoff,name="sair"),
    path('adicionar_despesa',views.add_gasto,name="add_despesa"),
    path('adicionar_deposito',views.add_deposito,name='add_deposito'),
    path('adicionar_meta',views.add_meta_financeira,name="add_meta"),
    path('editar_teto',views.add_teto_gasto,name="edit_teto"),
    path('vizualizar_historico/<int:id>',views.treat_route,name="view_history"),
    path('vizualizar_gastos',views.view_all_despesas,name="view_all_gastos"),
    path('editar_despesa/<int:id>',views.edit_despesa,name="edit_despesa"),
    path('visualizar_despesas_por_categoria',views.view_despesa_por_categoria,name="despesa_por_categoria"),
    path('visualizar_despesa_por_data',views.view_despesa_por_data,name="despesa_por_data"),
    path('get/gastos_por_mes',views.get_despesas_agrupadas_por_mes_grafico,name="gastos_por_mes")
]
