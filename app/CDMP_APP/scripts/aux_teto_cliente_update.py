from .. import models

def update_teto_gastos(objeto_teto_atual:models.TetoDeGastos,form_teto:models.TetoDeGastos):
    if objeto_teto_atual.cliente ==None:
        form_teto.janeiro=objeto_teto_atual.janeiro
        form_teto.fevereiro=objeto_teto_atual.fevereiro
        form_teto.marco=objeto_teto_atual.marco
        form_teto.abril=objeto_teto_atual.abril
        form_teto.maio=objeto_teto_atual.maio
        form_teto.junho=objeto_teto_atual.junho
        form_teto.julho=objeto_teto_atual.julho
        form_teto.agosto=objeto_teto_atual.agosto
        form_teto.setembro=objeto_teto_atual.setembro
        form_teto.outubro=objeto_teto_atual.outubro
        form_teto.novembro=objeto_teto_atual.novembro
        form_teto.dezembro=objeto_teto_atual.dezembro
    else:
        objeto_teto_atual.janeiro=form_teto.janeiro
        objeto_teto_atual.fevereiro=form_teto.fevereiro
        objeto_teto_atual.marco=form_teto.marco
        objeto_teto_atual.abril=form_teto.abril
        objeto_teto_atual.maio=form_teto.maio
        objeto_teto_atual.junho=form_teto.junho
        objeto_teto_atual.julho=form_teto.julho
        objeto_teto_atual.agosto=form_teto.agosto
        objeto_teto_atual.setembro=form_teto.setembro
        objeto_teto_atual.outubro=form_teto.outubro
        objeto_teto_atual.novembro=form_teto.novembro
        objeto_teto_atual.dezembro=form_teto.dezembro

def update_teto_gastos_por_geral(model_teto:models.TetoDeGastos,valor_geral):
    if isinstance(valor_geral,(int,float)):
        model_teto.janeiro=valor_geral
        model_teto.fevereiro=valor_geral
        model_teto.marco=valor_geral
        model_teto.abril=valor_geral
        model_teto.maio=valor_geral
        model_teto.junho=valor_geral
        model_teto.julho=valor_geral
        model_teto.agosto=valor_geral
        model_teto.setembro=valor_geral
        model_teto.outubro=valor_geral
        model_teto.novembro=valor_geral
        model_teto.dezembro=valor_geral
    else:
        raise TypeError("Only integer or float are allowed") 