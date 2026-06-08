from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from service.admin_service import obter_estatisticas_admin

api_admin = Blueprint('api_admin', __name__, url_prefix='/api/admin')


@api_admin.route('/')
@login_required
def painel():
    if current_user.role != 'admin' and current_user.email != 'fintrack@admin.com':
        return jsonify({'erro': 'Acesso negado.'}), 403
    d = obter_estatisticas_admin()
    return jsonify({
        'total_usuarios': d['total_usuarios'],
        'usuarios_ativos': d['usuarios_ativos'],
        'total_boletos': d['total_boletos'],
        'total_assinaturas': d['total_assinaturas'],
        'total_gastos': d['total_gastos'],
        'volume_boletos': float(d['volume_boletos']),
        'volume_assinaturas': float(d['volume_assinaturas']),
        'volume_gastos': float(d['volume_gastos']),
        'volume_total': float(d['volume_total']),
    })
