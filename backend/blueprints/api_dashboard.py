from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from service.dashboard_service import montar_dashboard

api_dashboard = Blueprint('api_dashboard', __name__, url_prefix='/api/dashboard')


@api_dashboard.route('/')
@login_required
def painel():
    d = montar_dashboard(current_user.id)
    hoje = d['today']

    boletos_urgentes = [{
        'id': b.id,
        'nome': b.nome,
        'valor': float(b.valor),
        'vencimento': b.vencimento.strftime('%d/%m/%Y'),
        'dias': (b.vencimento - hoje).days,
    } for b in d['boletos_urgentes']]

    gastos_recentes = [{
        'descricao': g.descricao,
        'valor': float(g.valor),
        'categoria': g.categoria.nome if g.categoria else None,
        'data': g.data.strftime('%d/%m/%Y'),
    } for g in d['gastos_recentes']]

    return jsonify({
        'total_boletos': float(d['total_boletos']),
        'total_assinaturas': float(d['total_assinaturas']),
        'total_gastos_mes': float(d['total_gastos_mes']),
        'total_mensal': float(d['total_mensal']),
        'qtd_boletos_pendentes': d['qtd_boletos_pendentes'],
        'qtd_assinaturas_ativas': d['qtd_assinaturas_ativas'],
        'qtd_alertas': d['qtd_alertas'],
        'boletos_urgentes': boletos_urgentes,
        'gastos_recentes': gastos_recentes,
    })
