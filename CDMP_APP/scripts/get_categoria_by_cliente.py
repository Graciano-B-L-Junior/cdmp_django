
from CDMP_APP.models import Categoria

def set_choices_categoria(cliente) -> tuple:
        categorias = Categoria.objects.filter(
              cliente__pk=cliente
        )
        tupla= tuple()
        lista=[]
        for categoria in categorias:
              lista.append(categoria.nome)
        tupla = ((categoria,categoria) for categoria in lista)
        return tupla