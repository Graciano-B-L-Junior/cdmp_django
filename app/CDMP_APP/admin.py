from django.contrib import admin

# Register your models here.
from .models import Categoria,Cliente,Receitas,Despesa,HistoricoCliente,TetoDeGastos


class ClienteAdmin(admin.ModelAdmin):
    list_display=["nome","email","foto"]

class HistoricoClienteAdmin(admin.ModelAdmin):
    list_display=["cliente","operacao","data_operacao"]
    


admin.site.register(Categoria)
admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Receitas)
admin.site.register(Despesa)
admin.site.register(HistoricoCliente,HistoricoClienteAdmin)
admin.site.register(TetoDeGastos)