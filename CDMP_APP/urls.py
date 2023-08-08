from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('adicionar_gasto',views.add_gasto,name="add_gasto")
]
