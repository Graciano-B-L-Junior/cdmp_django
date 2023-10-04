
import json
from django.http import HttpResponse
from CDMP_APP import models


def get_all_despesas_by_user(request):
    cliente = request.session.get("cliente")
    class Table():
        def __init__(self,descricao,valor,data,categoria,historico_id) -> None:
            self.descricao = descricao
            self.valor = valor
            self.data = data
            self.categoria = categoria
            self.historico_id = historico_id
            pass
    if cliente!=None:
        historicos = models.HistoricoCliente.objects.filter(
            cliente=models.Cliente.objects.get(pk=cliente),
            despesa__isnull=False,
            receita__isnull=True,
        )
        response={}
        despesas=[]
        for historico in historicos:
            # response[historico.despesa.pk]={
            #     "descricao":historico.despesa.descricao,
            #     "valor":historico.despesa.valor,
            #     "data":historico.despesa.data_despesa.strftime("%d-%m-%Y"),
            #     "categoria":historico.despesa.categoria.nome,
            #     "historico_id":historico.pk
            # }
            despesas.append(
                Table(
                    historico.despesa.descricao,
                    historico.despesa.valor,
                    historico.despesa.data_despesa.strftime("%d/%m/%Y"),
                    historico.despesa.categoria.nome,
                    historico.pk
                )
            )
        return despesas
    else:
        raise Exception("usuario não logado")