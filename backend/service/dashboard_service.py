from datetime import date
import calendar
from repository.assinatura_repository import listar_assinaturas
from repository.gasto_repository import listar_gastos, total_mes_atual
from repository.categoria_repository import listar_categorias
from repository.boleto_repository import listar_boletos


def proximo_vencimento(dia, hoje):
    ultimo_dia_mes_atual = calendar.monthrange(hoje.year, hoje.month)[1]
    dia_efetivo = min(dia, ultimo_dia_mes_atual)
    if dia_efetivo >= hoje.day:
        return hoje.replace(day=dia_efetivo)
    if hoje.month == 12:
        ano, mes = hoje.year + 1, 1
    else:
        ano, mes = hoje.year, hoje.month + 1
    ultimo_dia_prox_mes = calendar.monthrange(ano, mes)[1]
    dia_efetivo = min(dia, ultimo_dia_prox_mes)
    return date(ano, mes, dia_efetivo)


def montar_dashboard(usuario_id):
    hoje = date.today()
    assinaturas = listar_assinaturas(usuario_id)
    gastos = listar_gastos(usuario_id)
    categorias = listar_categorias(usuario_id)
    boletos = listar_boletos(usuario_id)

    total_assinaturas = sum(a.valor_mensal() for a in assinaturas if a.status == 'ativa')
    total_gastos_mes = total_mes_atual(usuario_id)
    total_mensal = total_assinaturas + total_gastos_mes
    total_boletos_val = sum(b.valor for b in boletos if b.status == 'pendente')
    qtd_boletos_pendentes = len([b for b in boletos if b.status == 'pendente'])
    qtd_assinaturas_ativas = len([a for a in assinaturas if a.status == 'ativa'])

    alertas = []
    for b in boletos:
        if b.status == 'pendente':
         dias = (b.vencimento - hoje).days
         if 0 <= dias <= 7:
            alertas.append({'tipo': 'boleto', 'obj': b, 'dias': dias, 'vencimento': b.vencimento})
    for a in assinaturas:
        if a.status == 'ativa' and a.dia_vencimento:
            vencimento = proximo_vencimento(a.dia_vencimento, hoje)
            dias = (vencimento - hoje).days
            if dias <= 7:
                alertas.append({'tipo': 'assinatura', 'obj': a, 'dias': dias, 'vencimento': vencimento})
    alertas.sort(key=lambda x: x['dias'])

    boletos_urgentes = sorted(
        [b for b in boletos if b.status == 'pendente' and (b.vencimento - hoje).days <= 7],
        key=lambda b: b.vencimento
    )

    gastos_recentes = sorted(gastos, key=lambda g: g.data, reverse=True)[:5]

    gasto_categoria = {}
    for a in assinaturas:
        if a.status == 'ativa' and a.categoria:
            chave = a.categoria.nome
            gasto_categoria[chave] = gasto_categoria.get(chave, 0) + a.valor_mensal()
    for g in gastos:
        if g.categoria:
            chave = g.categoria.nome
            gasto_categoria[chave] = gasto_categoria.get(chave, 0) + g.valor

    chart_labels = list(gasto_categoria.keys())
    chart_values = list(gasto_categoria.values())
    cores_padrao = ['#4f8ef7','#3ecf8e','#f59e0b','#f7645a','#a78bfa',
                    '#20d9d2','#fb923c','#e879f9','#34d399','#f472b6']
    chart_colors = [c.cor if c.cor else cores_padrao[i % len(cores_padrao)]
                    for i, c in enumerate(categorias)][:len(chart_labels)]
    if not chart_colors:
        chart_colors = cores_padrao[:len(chart_labels)]

    return {
        'assinaturas': assinaturas,
        'gastos_recentes': gastos_recentes,
        'alertas': alertas,
        'boletos_urgentes': boletos_urgentes,
        'today': hoje,
        'total_mensal': total_mensal,
        'total_assinaturas': total_assinaturas,
        'total_gastos_mes': total_gastos_mes,
        'total_boletos': total_boletos_val,
        'qtd_boletos_pendentes': qtd_boletos_pendentes,
        'qtd_boletos_urgentes': len(boletos_urgentes),
        'qtd_assinaturas_ativas': qtd_assinaturas_ativas,
        'gasto_categoria': gasto_categoria,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
        'chart_colors': chart_colors,
        'qtd_alertas': len(alertas),
    }
