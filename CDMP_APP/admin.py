from django.contrib import admin

# Register your models here.
from .models import Categoria,Cliente,Depositos,Gasto,MetaFinanceira,HistoricoCliente


class ClienteAdmin(admin.ModelAdmin):
    list_display=["nome","email","foto"]
    


admin.site.register(Categoria)
admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Depositos)
admin.site.register(Gasto)
admin.site.register(HistoricoCliente)
admin.site.register(MetaFinanceira)