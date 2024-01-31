from .. import models
from datetime import datetime

def generate_Categories(cliente:models.Cliente):
    categoria=models.Categoria(nome="Lazer",data_criacao=datetime.now(),cliente=cliente)
    categoria.save()
    models.TetoDeGastosPorCategoria(cliente=cliente,categoria=categoria).save()

    categoria=models.Categoria(nome="Pessoal",data_criacao=datetime.now(),cliente=cliente)
    categoria.save()
    models.TetoDeGastosPorCategoria(cliente=cliente,categoria=categoria).save()

    categoria=models.Categoria(nome="Comida",data_criacao=datetime.now(),cliente=cliente)
    categoria.save()
    models.TetoDeGastosPorCategoria(cliente=cliente,categoria=categoria).save()

    categoria=models.Categoria(nome="Pets",data_criacao=datetime.now(),cliente=cliente)
    categoria.save()
    models.TetoDeGastosPorCategoria(cliente=cliente,categoria=categoria).save()

    categoria=models.Categoria(nome="Casa",data_criacao=datetime.now(),cliente=cliente)
    categoria.save()
    models.TetoDeGastosPorCategoria(cliente=cliente,categoria=categoria).save()