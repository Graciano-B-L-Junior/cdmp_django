from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('cadastrar_conta',views.cadastro,name='cadastrar'),
    path('home',views.index,name='index'),
    path('sair',views.logoff,name="sair"),
    path('adicionar_despesa',views.add_gasto,name="add_despesa"),
    path('adicionar_deposito',views.add_receita,name='add_receita'),
    path('adicionar_categoria',views.cadastrar_categoria,name='add_categoria'),
    path('editar_teto',views.add_teto_gasto,name="edit_teto"),
    path('editar_teto_categoria',views.set_teto_categoria,name="set_teto_categoria"),
    path('vizualizar_historico/<int:id>',views.treat_route,name="view_history"),
    path('vizualizar_gastos',views.view_all_despesas,name="view_all_gastos"),
    path('editar_despesa/<int:id>',views.edit_despesa,name="edit_despesa"),
    path('visualizar_despesas_por_categoria',views.view_despesa_por_categoria,name="despesa_por_categoria"),
    path('visualizar_despesa_por_data',views.view_despesa_por_data,name="despesa_por_data"),
    path('get/gastos_por_mes',views.get_despesas_agrupadas_por_mes_grafico,name="gastos_por_mes"),
    path('get/economias_por_mes',views.get_economia_despesas_agrupadas_por_mes_grafico,name="economias_por_mes"),
    path('get/gastos_por_categoria',views.get_gastos_por_categoria,name="gastos_por_categoria"),
    path('get/gastos_por_categoria_x_teto_categoria',views.get_gastos_categoria_x_teto_gastos_categoria,name="categoria_x_teto_categoria"),
    #path('get/all_despesas',views.get_all_despesas,name="get_all_despesas"),
]
